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
from typing import TYPE_CHECKING, Union
from cl.runtime.data.record import Record
if TYPE_CHECKING:
    from stubs.cl.runtime.data.attrs.stub_attrs_cyclic_b import StubAttrsCyclicB


@attrs_data
class StubAttrsCyclicA(Record):
    """Stub class A with a field whose type is key for class B."""

    a_id: str = attrs_field()
    """Unique identifier."""

    b: Union[str, StubAttrsCyclicB] = attrs_field()
    """Key for class B."""

    @staticmethod
    def create() -> StubAttrsCyclicA:
        """Create an instance of this class populated with sample data."""

        # Import inside function to avoid cyclic reference error
        from stubs.cl.runtime.data.attrs.stub_attrs_cyclic_b import StubAttrsCyclicB

        obj = StubAttrsCyclicA()
        obj.a_id = "abc"
        obj.b = StubAttrsCyclicB()
        obj.b.b_id = "xyz"
        return obj
