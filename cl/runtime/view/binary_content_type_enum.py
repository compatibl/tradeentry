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

    Jpg = 0
    """Jpg image type."""

    Jpeg = 1
    """Jpeg image type."""

    Html = 2
    """Html content type."""

    Plotly = 3
    """The output provided by Plotly Graphing Library."""

    Png = 4
    """PNG image type."""

    Svg = 5
    """SVG image type."""

    Csv = 6
    """Csv type."""

    Zip = 7
    """Zip type."""

    Pdf = 8
    """PDF type."""

    Xlsx = 9
    """Excel type."""
