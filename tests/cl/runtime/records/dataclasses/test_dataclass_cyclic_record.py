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
from stubs.cl.runtime.records.dataclasses.stub_dataclass_cyclic_a_key import StubDataclassCyclicAKey
from stubs.cl.runtime.records.dataclasses.stub_dataclass_cyclic_b import StubDataclassCyclicB
from stubs.cl.runtime.records.dataclasses.stub_dataclass_cyclic_b_key import StubDataclassCyclicBKey


def test_cyclic_record():
    """Test for a cyclic import where classes StubDataclassCyclicA and StubDataclassCyclicB reference each other."""

    # Create inside the class with import inside function
    a_1 = StubDataclassCyclicA.create()
    b_1 = StubDataclassCyclicB.create()

    # Create A outside the class
    a_2 = StubDataclassCyclicA()
    a_2.b_obj = StubDataclassCyclicB.create()

    # Create B outside the class
    b_2 = StubDataclassCyclicB()
    b_2.a_obj = StubDataclassCyclicA.create()

    # Test for annotation introspection
    assert StubDataclassCyclicAKey.__annotations__ == {
        "b_key": StubDataclassCyclicBKey,
    }
    assert StubDataclassCyclicA.__annotations__ == {
        "b_obj": "StubDataclassCyclicB",
    }
    assert StubDataclassCyclicBKey.__annotations__ == {
        "str_id": str,
    }
    assert StubDataclassCyclicB.__annotations__ == {
        "a_obj": "StubDataclassCyclicA",
    }

    # Test for keys

    assert b_1.get_key() == StubDataclassCyclicBKey("a")
    assert a_1.get_key() == StubDataclassCyclicAKey(StubDataclassCyclicBKey("b"))
    pass


if __name__ == "__main__":
    pytest.main([__file__])
