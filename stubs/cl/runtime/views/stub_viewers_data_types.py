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

import os.path
from dataclasses import dataclass
from logging import getLogger
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.views.binary_content import BinaryContent
from cl.runtime.views.binary_content_type_enum import BinaryContentTypeEnum
from cl.runtime.view.dag.dag import Dag
from cl.runtime.view.dag.dag_edge import DagEdge
from cl.runtime.view.dag.dag_layout_enum import DagLayoutEnum
from cl.runtime.view.dag.dag_node_data import DagNodeData
from cl.runtime.view.dag.nodes.add_text_node import AddTextNode
from cl.runtime.view.dag.nodes.text_input_node import TextInputNode
from cl.runtime.view.dag.nodes.text_output_node import TextOutputNode
from stubs.cl.runtime.views.stub_viewers_data_types_key import StubViewersDataTypesKey

_logger = getLogger(__name__)


@dataclass(slots=True, kw_only=True)
class StubViewersDataTypes(StubViewersDataTypesKey, RecordMixin[StubViewersDataTypesKey]):
    """Stub record base class."""

    def get_key(self) -> StubViewersDataTypesKey:
        return StubViewersDataTypesKey(stub_id=self.stub_id)

    def view_pdf(self) -> BinaryContent:
        """Shows a PDF document."""

        file_path = os.path.join(os.path.dirname(__file__), "stub_viewers_data_types.pdf")
        with open(file_path, mode="rb") as file:
            content = file.read()
        pdf_content = BinaryContent(content=content, content_type=BinaryContentTypeEnum.PDF)
        return pdf_content

    def view_graph(self) -> Dag:
        """Shows a directed acyclic graph."""

        dag = Dag(
            name="dag_data",
            nodes=[
                TextInputNode(id_="root", text="root", data=DagNodeData(label="Input")),
                AddTextNode(id_="a", text_to_add="add A", data=DagNodeData(label="A")),
                AddTextNode(id_="b", text_to_add="add B", data=DagNodeData(label="B")),
                AddTextNode(id_="c", text_to_add="add C", data=DagNodeData(label="C")),
                AddTextNode(id_="d", text_to_add="add D", data=DagNodeData(label="D")),
                AddTextNode(id_="e", text_to_add="add E", data=DagNodeData(label="E")),
                TextOutputNode(id_="output1", data=DagNodeData(label="Output 1")),
                TextOutputNode(id_="output2", data=DagNodeData(label="Output 2")),
            ],
            edges=[
                DagEdge(source="root", target="a", id_="root;a", label="main stream"),
                DagEdge(source="a", target="b", id_="a;b", label="filtered stream"),
                DagEdge(source="a", target="e", id_="a;e", label="main stream"),
                DagEdge(source="e", target="output1", id_="e;output1", label="to text"),
                DagEdge(source="e", target="output2", id_="e;output2", label="to file"),
                DagEdge(source="d", target="output2", id_="d;output2", label="to file"),
                DagEdge(source="d", target="e", id_="d;e"),
                DagEdge(source="c", target="d", id_="c;d"),
                DagEdge(source="b", target="c", id_="b;c"),
            ],
        )

        return Dag.auto_layout_dag(dag, layout_mode=DagLayoutEnum.PLANAR, base_scale=180)
