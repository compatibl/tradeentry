# Copyright (C) 2023-present The Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing_extensions import Self

from cl.convince.entries.entry_type_key import EntryTypeKey
from cl.runtime import Context
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.primitive.char_util import CharUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.view.dag.dag import Dag
from cl.runtime.view.dag.dag_edge import DagEdge
from cl.runtime.view.dag.dag_layout_enum import DagLayoutEnum
from cl.runtime.view.dag.dag_node_data import DagNodeData
from cl.runtime.view.dag.nodes.dag_node import DagNode
from cl.convince.entries.entry_key import EntryKey
from cl.convince.entries.entry_status_enum import EntryStatusEnum
from cl.convince.entries.entry_util import EntryUtil


@dataclass(slots=True, kw_only=True)
class Entry(EntryKey, RecordMixin[EntryKey], ABC):
    """Contains title, body and supporting data of user entry along with the entry processing result."""

    entry_type: EntryTypeKey = missing()
    """Type of the entry (included in MD5 hash)."""

    title: str = missing()
    """Title of a long entry or complete description of a short one (included in MD5 hash)."""

    body: str | None = None
    """Optional body of the entry if not completely described by the title (included in MD5 hash)."""

    data: str | None = None
    """Optional supporting data in YAML format (included in MD5 hash)."""

    approved_by: UserKey | None = None
    """Use who recorded the approval."""

    def get_key(self) -> EntryKey:
        return EntryKey(entry_id=self.entry_id)

    def init(self) -> None:
        """Generate entry_id in 'type: title' format followed by an MD5 hash of body and data if present."""

        # Set entry_id based on the type, title, body and data of the record
        self.entry_id = EntryUtil.create_id(self.entry_type, self.title, body=self.body, data=self.data)

    @abstractmethod
    def run_propose(self) -> None:
        """Generate or regenerate the proposed value."""

    def run_approve(self) -> None:
        """Approve the manually set approved value, or proposed value if the approved value is not set."""
        # Set approved_py to the user obtained from the current context and save
        context = Context.current()
        self.approved_by = context.user
        context.save_one(self)

    @staticmethod
    def build_dag(
        entry: "Entry",
        layout_mode: DagLayoutEnum = DagLayoutEnum.PLANAR,
        ignore_fields: list[str] = None,
    ) -> Dag:
        """Build the DAG for the entry."""
        ignore_fields = ignore_fields or []
        nodes, edges = [entry.to_dag_node()], []

        def traverse_graph_from_node(entry_record: Entry, source_node: DagNode):
            """Traverse the graph from the specified node."""
            if not (slots := getattr(entry_record, "__slots__", None)):
                return

            entry_fields = {
                field_name: field_value
                for field_name in slots
                if (
                    isinstance((field_value := getattr(entry_record, field_name)), EntryKey)
                    # TODO (Yauheni): Use declarations instead of isinstance
                    # TODO: (Yauheni): Current filtration filters out the empty lists, which should be processed
                    or (field_value and hasattr(field_value, "__iter__") and isinstance(field_value[0], EntryKey))
                    and field_name not in ignore_fields
                )
            }
            for field_name, field_value in entry_fields.items():
                if isinstance(field_value, EntryKey):
                    if not (entry := Context.current().load_one(EntryKey, field_value)):
                        Entry.__append_empty_node(
                            source_node=source_node,
                            entry_id=field_value.entry_id,
                            edge_label=CaseUtil.snake_to_title_case(field_name),
                            nodes=nodes,
                            edges=edges,
                        )
                        continue

                    entry_node = entry.to_dag_node()
                    edges.append(
                        Dag.build_edge_between_nodes(
                            source=source_node,
                            target=entry_node,
                            label=CaseUtil.snake_to_title_case(field_name),
                        ),
                    )
                    if entry_node not in nodes:
                        nodes.append(entry_node)
                        traverse_graph_from_node(entry_record=field_value, source_node=entry_node)
                else:
                    if not field_value:
                        # TODO (Yauheni): Handle the case, when the list is empty
                        continue

                    for index, entry_key in enumerate(field_value, start=1):
                        if not (entry := Context.current().load_one(EntryKey, entry_key)):
                            Entry.__append_empty_node(
                                source_node=source_node,
                                entry_id=field_value.entry_id,
                                edge_label=f"{CaseUtil.snake_to_title_case(field_name)}[{index}]",
                                nodes=nodes,
                                edges=edges,
                            )
                            continue

                        entry_node = entry.to_dag_node()
                        edges.append(
                            Dag.build_edge_between_nodes(
                                source=source_node,
                                target=entry_node,
                                label=f"{CaseUtil.snake_to_title_case(field_name)}[{index}]",
                            ),
                        )
                        if entry_node not in nodes:
                            nodes.append(entry_node)
                            traverse_graph_from_node(entry_record=entry, source_node=entry_node)

        traverse_graph_from_node(entry, nodes[0])
        dag = Dag(name=f"DAG from `{entry.entry_id}` node", nodes=nodes, edges=edges)

        return Dag.auto_layout_dag(dag, layout_mode)

    def to_dag_node(self) -> DagNode:
        """Transform entry to DAG node."""
        return DagNode(id_=self.entry_id, data=DagNodeData(label=self.entry_id))

    @staticmethod
    def __append_empty_node(
        source_node: DagNode,
        entry_id: str,
        edge_label: str,
        nodes: list[DagNode],
        edges: list[DagEdge],
    ) -> None:
        """Append empty node to the list of nodes and edge to the list of edges."""
        # TODO (Yauheni): Add color information to the node with entry, which doesn't exist
        empty_node = DagNode(id_=entry_id, data=DagNodeData(label=entry_id))
        if empty_node not in nodes:
            nodes.append(empty_node)
        edges.append(
            Dag.build_edge_between_nodes(source=source_node, target=empty_node, label=edge_label),
        )
