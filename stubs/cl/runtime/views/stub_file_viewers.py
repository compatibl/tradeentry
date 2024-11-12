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
from cl.runtime.views.pdf_view import PdfView
from stubs.cl.runtime.views.stub_viewers import StubViewers


@dataclass(slots=True, kw_only=True)
class StubFileViewers(StubViewers):
    """Stub viewers for file content."""

    def view_markdown(self):
        """Viewer returning Markdown."""
        return {
            "_t": "Script",
            "Name": None,
            "Language": "Markdown",
            "Body": ["# Viewer with UI element", "### _Script_"],
            "WordWrap": None,
        }

    def _view_pdf(self):  # TODO: Not supported in this release
        """Stub viewer returning a PDF document."""
        file_path = os.path.join(os.path.dirname(__file__), "stub_data_viewers.pdf")
        with open(file_path, mode="rb") as file:
            content = file.read()
        return PdfView(pdf_bytes=content)
