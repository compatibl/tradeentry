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

import pytest
from stubs.cl.runtime.records.dataclasses.stub_dataclass_cyclic_a import StubDataclassCyclicA
from stubs.cl.runtime.records.dataclasses.stub_dataclass_cyclic_b import StubDataclassCyclicB


def test_cyclic_record():
    """Test for a cyclic import where classes StubDataclassCyclicA and StubDataclassCyclicB reference each other."""

    # Create inside the class with import inside function
    a_1 = StubDataclassCyclicA.create()
    b_1 = StubDataclassCyclicB.create()

    # Create A outside the class
    a_2 = StubDataclassCyclicA()
    a_2.b = StubDataclassCyclicB.create()

    # Create B outside the class
    b_2 = StubDataclassCyclicB()
    b_2.a = StubDataclassCyclicA.create()

    # Test for annotation introspection
    assert StubDataclassCyclicA.__annotations__ == {
        "key": "StubDataclassCyclicBKey | None",
        "b": "StubDataclassCyclicB | None",
    }
    assert StubDataclassCyclicB.__annotations__ == {"id": "str | None", "a": "StubDataclassCyclicA | None"}

    # Test for keys

    assert b_1.get_base_type() == StubDataclassCyclicB
    assert b_1.get_key() == (StubDataclassCyclicB, "a")
    assert a_1.get_base_type() == StubDataclassCyclicA
    assert a_1.get_key() == (StubDataclassCyclicA, (StubDataclassCyclicB, "b"))
    pass


if __name__ == "__main__":
    pytest.main([__file__])
