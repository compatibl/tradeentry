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
from cl.runtime.decorators.viewer_decorator import viewer
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.view.binary_content import BinaryContent
from cl.runtime.view.binary_content_type_enum import BinaryContentTypeEnum
from stubs.cl.runtime.views.stub_viewers_data_types_key import StubViewersDataTypesKey

_logger = getLogger(__name__)


@dataclass(slots=True, kw_only=True)
class StubViewersDataTypes(StubViewersDataTypesKey, RecordMixin[StubViewersDataTypesKey]):
    """Stub record base class."""

    def get_key(self) -> StubViewersDataTypesKey:
        return StubViewersDataTypesKey(stub_id=self.stub_id)

    @viewer
    def pdf_viewer(self) -> BinaryContent:
        """Shows a PDF document."""

        file_path = os.path.join(os.path.dirname(__file__), "stub_viewers_data_types.pdf")
        with open(file_path, mode="rb") as file:
            content = file.read()
        pdf_content = BinaryContent(content=content, content_type=BinaryContentTypeEnum.Pdf)
        return pdf_content
