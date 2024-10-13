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
from cl.runtime import Context
from cl.runtime import RecordMixin
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.view.dag.dag import Dag
from cl.runtime.views.dag.successor_dag_key import SuccessorDagKey
from cl.runtime.views.dag.successor_dag_node import SuccessorDagNode
from cl.runtime.views.dag.successor_dag_node_key import SuccessorDagNodeKey


@dataclass(slots=True, kw_only=True)
class SuccessorDag(SuccessorDagKey, RecordMixin[SuccessorDagKey]):
    """Directed acyclic graph (DAG) where each node defines its successors."""

    title: str = missing()
    """Title of the DAG."""

    root_node: SuccessorDagNodeKey = missing()
    """Root node of the DAG."""

    def get_key(self) -> SuccessorDagKey:
        return SuccessorDagKey(dag_id=self.dag_id)

    def view_dag(self) -> Dag | None:
        """DAG view for the decision tree node."""
        if self.root_node is None:
            return None

        root_node = Context.current().load_one(SuccessorDagNodeKey, self.root_node)

        if root_node is None:
            return None

        return SuccessorDagNode.build_dag(node=root_node)
