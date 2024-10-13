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

from dataclasses import dataclass
from typing import List
from typing import Optional
from cl.runtime import Context
from cl.runtime import RecordMixin
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.view.dag.dag import Dag
from cl.runtime.view.dag.dag_edge import DagEdge
from cl.runtime.view.dag.dag_layout_enum import DagLayoutEnum
from cl.runtime.view.dag.dag_node_data import DagNodeData
from cl.runtime.view.dag.nodes.dag_node import DagNode
from cl.runtime.views.dag.successor_dag_key import SuccessorDagKey
from cl.runtime.views.dag.successor_dag_node_key import SuccessorDagNodeKey


@dataclass(slots=True, kw_only=True)
class SuccessorDagNode(SuccessorDagNodeKey, RecordMixin[SuccessorDagNodeKey]):
    """Single node of SuccessorDag, defines its successors."""

    dag: SuccessorDagKey = missing()
    """The DAG this node belongs to (included in node_id)."""

    dag_node_id: str = missing()
    """Unique node identifier within the dag (included in node_id)."""

    node_yaml: str = missing()
    """Node details in YAML format."""

    successor_nodes: List[SuccessorDagNodeKey] | None = None
    """List of successor nodes (must belong to the same DAG)."""

    successor_edges: List[str] | None = None
    """List of successor edge names in the same order as successor_nodes (must have the same size if not None)."""

    def init(self) -> None:
        # Generate from dag_id and node_name fields
        self.node_id = f"{self.dag.dag_id}: {self.dag_node_id}"

        # TODO: Make this a standard feature of CSV reader, then remove this code
        if self.successor_nodes is not None:
            self.successor_nodes = [
                SuccessorDagNodeKey(**x) if isinstance(x, dict) else x for x in self.successor_nodes
            ]

        # Verify that each successor belongs to the same DAG
        if self.successor_nodes:
            offending_list = [s for s in self.successor_nodes if s.node_id.split(":")[0] != self.dag.dag_id]
            if offending_list and any(offending_list):
                offending_list_str = "  - ".join(f"  - Node: {x.node_id}\n" for x in offending_list)
                raise UserError(
                    f"One or more successors do not belong to DAG {self.dag.dag_id}:\n" f"{offending_list_str}"
                )
        # Verify that edges is None or has the same size
        edge_count = len(self.successor_edges) if self.successor_edges is not None else 0
        successor_count = len(self.successor_nodes) if self.successor_nodes is not None else 0
        if False and edge_count != successor_count:
            raise UserError(
                f"In DAG node {self.node_id}, the number of edges is {edge_count} "
                f"which does not match number of successors {successor_count}."
            )

    def get_key(self) -> SuccessorDagNodeKey:
        return SuccessorDagNodeKey(node_id=self.node_id)

    def view_dag(self) -> Dag:
        """DAG view for the decision tree node."""
        return self.build_dag(node=self)

    @staticmethod
    def build_dag(
        node: "SuccessorDagNode",
        layout_mode: DagLayoutEnum = DagLayoutEnum.PLANAR,
        ignore_fields: Optional[list[str]] = None,
    ) -> Dag:
        """Build the DAG for the given node.

        Args:
            node (SuccessorDagNode): The root node to start the DAG from.
            layout_mode (DagLayoutEnum): Layout mode for arranging the DAG. Defaults to DagLayoutEnum.PLANAR.
            ignore_fields (Optional[list[str]]): Fields to ignore during traversal. Defaults to an empty list.

        Returns:
            Dag: The constructed directed acyclic graph (DAG).
        """
        ignore_fields = ignore_fields or []
        nodes, edges = [node.to_dag_node()], []

        def traverse_graph_from_node(node_record: SuccessorDagNode, source_node: DagNode):
            """Recursively traverse the graph starting from the given node.

            Args:
                node_record (SuccessorDagNode): The node to start traversal from.
                source_node (DagNode): The corresponding DAG node.
            """
            slots = getattr(node_record, "__slots__", None)
            if not slots:
                return

            node_fields = {
                field_name: field_value
                for field_name in slots
                if (
                    isinstance((field_value := getattr(node_record, field_name)), SuccessorDagNodeKey)
                    # TODO (Yauheni): Use declarations instead of isinstance
                    # TODO: (Yauheni): Current filtration filters out the empty lists, which should be processed
                    or (
                        field_value
                        and hasattr(field_value, "__iter__")
                        and isinstance(field_value[0], SuccessorDagNodeKey)
                    )
                    and field_name not in ignore_fields
                )
            }

            for field_name, field_value in node_fields.items():
                if isinstance(field_value, SuccessorDagNodeKey):
                    loaded_node = Context.current().load_one(SuccessorDagNodeKey, field_value)
                    if loaded_node is None:
                        SuccessorDagNode.__append_empty_node(
                            source_node=source_node,
                            node_id=field_value.node_id,
                            edge_label=CaseUtil.snake_to_title_case(field_name),
                            nodes=nodes,
                            edges=edges,
                        )
                        continue

                    tree_node = loaded_node.to_dag_node()
                    edges.append(
                        Dag.build_edge_between_nodes(
                            source=source_node,
                            target=tree_node,
                            label=CaseUtil.snake_to_title_case(field_name),
                        )
                    )
                    if tree_node not in nodes:
                        nodes.append(tree_node)
                        traverse_graph_from_node(node_record=loaded_node, source_node=tree_node)
                else:
                    if not field_value:
                        continue

                    for index, node_key in enumerate(field_value, start=1):
                        edge_label = f"{CaseUtil.snake_to_title_case(field_name)}[{index}]"

                        if field_name.endswith("nodes"):
                            edges_names_field_name = field_name.rstrip("nodes") + "edges"
                            edges_names = getattr(node_record, edges_names_field_name, None)
                            if edges_names and len(edges_names) == len(field_value):
                                edge_label = edges_names[index - 1]

                        loaded_node = Context.current().load_one(SuccessorDagNodeKey, node_key)
                        if loaded_node is None:
                            SuccessorDagNode.__append_empty_node(
                                source_node=source_node,
                                node_id=node_key.node_id,
                                edge_label=edge_label,
                                nodes=nodes,
                                edges=edges,
                            )
                            continue

                        tree_node = loaded_node.to_dag_node()
                        edges.append(
                            Dag.build_edge_between_nodes(
                                source=source_node,
                                target=tree_node,
                                label=edge_label,
                            )
                        )
                        if tree_node not in nodes:
                            nodes.append(tree_node)
                            traverse_graph_from_node(node_record=loaded_node, source_node=tree_node)

        traverse_graph_from_node(node, nodes[0])
        dag = Dag(name=f"DAG from `{node.node_id}` node", nodes=nodes, edges=edges)
        return Dag.auto_layout_dag(dag, layout_mode)

    def to_dag_node(self) -> DagNode:
        """Transform tree node to the DAG node."""
        node_data = DagNodeData(label=self.node_id)
        node_data.node_data = {"title": self.node_id, "data": self.node_yaml}
        return DagNode(id_=self.node_id, data=node_data)

    @staticmethod
    def __append_empty_node(
        source_node: DagNode,
        node_id: str,
        edge_label: str,
        nodes: list[DagNode],
        edges: list[DagEdge],
    ) -> None:
        """Append empty node to the list of nodes and edge to the list of edges."""
        # TODO (Yauheni): Add color information to the node with entry, which doesn't exist
        empty_node = DagNode(id_=node_id, data=DagNodeData(label=node_id))
        if empty_node not in nodes:
            nodes.append(empty_node)
        edges.append(
            Dag.build_edge_between_nodes(source=source_node, target=empty_node, label=edge_label),
        )
