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
from cl.runtime.storage.stubs.stub_cyclic_a import StubCyclicA
from cl.runtime.storage.stubs.stub_cyclic_b import StubCyclicB


def test_cyclic_record():
    """Test for a cyclic import where classes StubCyclicA and StubCyclicB reference each other."""

    # Create test base_record and populate with sample data
    context = rt.Context()

    # Create inside the class with import inside function
    a_1 = StubCyclicA.create_sample_record(context)
    b_1 = StubCyclicB.create_sample_record(context)

    # Create A outside the class
    a_2 = StubCyclicA()
    a_2.context = context
    a_2.a_id = 'abc'
    a_2.b = StubCyclicB.create_key('abc')
    a_2.init()

    # Create B outside the class
    b_2 = StubCyclicB()
    b_2.context = context
    b_2.b_id = 'abc'
    b_2.a = StubCyclicA.create_key('abc')
    b_2.init()

    # Test for annotation retrospection
    assert StubCyclicA.__annotations__ == {'a_id': 'str', 'b': 'Union[str, StubCyclicB]'}
    assert StubCyclicB.__annotations__ == {'b_id': 'str', 'a': 'Union[str, StubCyclicA]'}


if __name__ == '__main__':
    pytest.main([__file__])
