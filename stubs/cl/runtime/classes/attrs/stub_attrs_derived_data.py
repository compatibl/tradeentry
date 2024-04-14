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

from cl.runtime.classes.attrs_util import data_class
from cl.runtime.classes.attrs_util import data_field
from stubs.cl.runtime.classes.attrs.stub_attrs_data import StubAttrsData
from typing import Optional


@data_class
class StubAttrsDerivedData(StubAttrsData):
    """Stub derived data type."""

    derived_field: str = data_field(default="derived")
    """Stub field."""
