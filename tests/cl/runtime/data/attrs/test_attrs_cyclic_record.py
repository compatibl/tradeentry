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
import cl.runtime as rt
from stubs.cl.runtime.data.attrs.stub_attrs_cyclic_a import StubAttrsCyclicA
from stubs.cl.runtime.data.attrs.stub_attrs_cyclic_b import StubAttrsCyclicB


def test_cyclic_record():
    """Test for a cyclic import where classes StubAttrsCyclicA and StubAttrsCyclicB reference each other."""

    # Create inside the class with import inside function
    a_1 = StubAttrsCyclicA.create()
    b_1 = StubAttrsCyclicB.create()

    # Create A outside the class
    a_2 = StubAttrsCyclicA()
    a_2.a_id = 'abc'
    a_2.b = StubAttrsCyclicB.create()

    # Create B outside the class
    b_2 = StubAttrsCyclicB()
    b_2.b_id = 'abc'
    b_2.a = StubAttrsCyclicA.create()

    # Test for annotation retrospection
    assert StubAttrsCyclicA.__annotations__ == {'a_id': 'str', 'b': 'Union[str, StubAttrsCyclicB]'}
    assert StubAttrsCyclicB.__annotations__ == {'b_id': 'str', 'a': 'Union[str, StubAttrsCyclicA]'}


if __name__ == '__main__':
    pytest.main([__file__])
