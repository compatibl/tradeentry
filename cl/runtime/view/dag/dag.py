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

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import networkx as nx

from cl.runtime import RecordMixin
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.view.dag.dag_edge import DAGEdge
from cl.runtime.view.dag.dag_key import DAGKey
from cl.runtime.view.dag.dag_layout_enum import DAGLayoutEnum
from cl.runtime.view.dag.dag_node_position import DAGNodePosition
from cl.runtime.view.dag.nodes.dag_node import DAGNode


@dataclass(slots=True, kw_only=True)
class DAG(DAGKey, RecordMixin[DAGKey]):
    """Representation of directed acyclic graph (DAG)."""

    nodes: List[DAGNode] = missing()
    """List of DAG nodes."""

    edges: List[DAGEdge] = missing()
    """List of DAG edges."""

    def get_key(self) -> DAGKey:
        """Return primary key of this instance in semicolon-delimited string format."""
        return DAGKey(name=self.name)

    @staticmethod
    def auto_layout_dag(
        dag: DAG,
        layout_mode: DAGLayoutEnum = DAGLayoutEnum.SPRING,
        offset_x: int = 600,
        base_scale: int = 100,
    ) -> DAG:
        """
        Set positions automatically for the passed DAG.

        Parameters
        ----------
            dag : DAG
                DAG to create layout for.
            layout_mode : DAGLayoutEnum
                Graph layout to use.
            offset_x : int
                Offset on x-axis to use between multiple DAGs. Won't affect the resulting autolayout of a single DAG.
            base_scale : int
                Base scale to use while calculating the final DAG scale.
                The final scale is calculated for each subgraph separately based on the number of nodes in
                it using the following formula: base_scale * number_of_nodes^0.5.

        Returns
        -------
            DAG
                A modified DAG object with adjusted positions of nodes.
        """

        subgraphs = dag._build_disconnected_graphs()
        positions = {}
        base_offset_x = 0.0

        for subgraph in subgraphs:
            subgraph_scale = base_scale * len(subgraph.nodes) ** 0.5

            if layout_mode == DAGLayoutEnum.CIRCULAR:
                layout = nx.circular_layout(subgraph, scale=subgraph_scale)
            elif layout_mode == DAGLayoutEnum.PLANAR:
                layout = nx.planar_layout(subgraph, scale=subgraph_scale)
            elif layout_mode == DAGLayoutEnum.SPRING:
                layout = nx.spring_layout(
                    subgraph,
                    scale=subgraph_scale,
                    # Number of iterations is for more accurate layout
                    iterations=100,
                    # Seed needed for consistent layout
                    seed=1,
                    # k - optimal distance between nodes, which should depend on the number of nodes
                    k=1 / (len(subgraph.nodes) ** 0.2),
                )
            else:
                raise Exception('Unsupported layout mode. Accepted layout modes: circular, planar, spring')
            positions.update({node: (x + base_offset_x, y) for node, (x, y) in layout.items()})
            base_offset_x += offset_x

        for node in dag.nodes:
            x, y = positions[node.id_]
            node.position = DAGNodePosition(x=float(x), y=float(y))

        return dag

    def _build_graph(self) -> nx.DiGraph:
        """Build networkx graph representation."""

        graph = nx.DiGraph(name=self.name)
        for edge in self.edges:
            graph.add_edge(**edge.to_networkx())
        for node in self.nodes:
            graph.add_node(**node.to_networkx())
        self._validate_graph(graph)
        return graph

    @staticmethod
    def _validate_graph(graph: nx.DiGraph):
        """Validate that graph has no cycles."""

        if not nx.is_directed_acyclic_graph(graph):
            raise RuntimeError("Graph is not acyclic!")

    def _build_disconnected_graphs(self) -> List[nx.DiGraph]:
        """Build list of disconnected (separated) networkx graphs."""

        graph = self._build_graph()
        return [graph.subgraph(subgraph) for subgraph in nx.weakly_connected_components(graph)]
