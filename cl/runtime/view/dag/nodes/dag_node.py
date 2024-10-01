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
from typing import Optional, Dict, Any

from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.view.dag.dag_node_position import DAGNodePosition
from cl.runtime.view.dag.dag_node_data import DAGNodeData


@dataclass(slots=True, kw_only=True)
class DAGNode:
    """
    Representation of the node of directed acyclic graph.
    """

    id_: str = missing()
    """Node unique identifier."""

    position: DAGNodePosition | None = missing()
    """Node UI position."""

    data: DAGNodeData = missing()
    """Node internal data."""

    def to_networkx(self) -> Dict[str, Any]:
        """Transform node to networkx representation."""
        result = {
            "node_for_adding": self.id_,
        }
        return result