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
from cl.runtime import RecordMixin
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.records.dataclasses_extensions import missing
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
                SuccessorDagNodeKey(**x) if isinstance(x, dict) else x
                for x in self.successor_nodes
            ]

        # Verify that each successor belongs to the same DAG
        if self.successor_nodes:
            offending_list = [s for s in self.successor_nodes if s.node_id.split(":")[0] != self.dag.dag_id]
            if offending_list and any(offending_list):
                offending_list_str = "  - ".join(f"  - Node: {x.node_id}\n" for x in offending_list)
                raise UserError(
                    f"One or more successors do not belong to DAG {self.dag.dag_id}:\n"
                    f"{offending_list_str}"
                )
        # Verify that edges is None or has the same size
        edge_count = len(self.successor_edges) if self.successor_edges is not None else 0
        successor_count = len(self.successor_nodes) if self.successor_nodes is not None else 0
        if False and edge_count != successor_count:
            raise UserError(f"In DAG node {self.node_id}, the number of edges is {edge_count} "
                            f"which does not match number of successors {successor_count}.")

    def get_key(self) -> SuccessorDagNodeKey:
        return SuccessorDagNodeKey(node_id=self.node_id)
