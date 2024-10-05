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

from enum import IntEnum


class BinaryContentTypeEnum(IntEnum):
    """Binary content type enumeration."""

    UNDEFINED = 0
    """Undefined content type."""

    JPG = 1
    """Jpg image type."""

    JPEG = 2
    """Jpeg image type."""

    HTML = 3
    """Html content type."""

    PLOTLY = 4
    """The output provided by Plotly Graphing Library."""

    PNG = 5
    """PNG image type."""

    SVG = 6
    """SVG image type."""

    CSV = 7
    """Csv type."""

    ZIP = 8
    """Zip type."""

    PDF = 9
    """PDF type."""

    XLSX = 10
    """Excel type."""
