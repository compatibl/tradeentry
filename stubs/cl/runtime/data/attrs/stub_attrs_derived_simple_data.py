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
from cl.runtime.data.attrs.attrs_data_util import attrs_data
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from stubs.cl.runtime.data.attrs.stub_attrs_simple_data import StubAttrsSimpleData


@attrs_data
class StubAttrsDerivedSimpleData(StubAttrsSimpleData):
    """Dataclass-based serializable data sample used in tests."""

    derived_field_str: str = attrs_field(default='def')
    """String attribute of base class."""

    derived_field_float: float = attrs_field(default=4.56)
    """Float attribute of base class."""

