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


def test_cyclic_record():
    """Test for a cyclic record definition where """

    # TODO: Determine if using string type hint or noqa is recommended for cyclic reference type hints

    # Create test base_record and populate with sample data
    context = rt.Context()
    
    # Create inside the class with import inside function
    a_1 = rt.stubs.StubCyclicA.create_sample_record(context)
    b_1 = rt.stubs.StubCyclicB.create_sample_record(context)
    
    # Create A outside the class
    a_2 = rt.stubs.StubCyclicA()
    a_2.context = context
    a_2.a_id = 'abc'
    a_2.b = rt.stubs.StubCyclicB.create_key('abc')
    a_2.update()

    # Create B outside the class
    b_2 = rt.stubs.StubCyclicB()
    b_2.context = context
    b_2.b_id = 'abc'
    b_2.a = rt.stubs.StubCyclicA.create_key('abc')
    b_2.update()

    # Test for annotation retrospection
    assert rt.stubs.StubCyclicA.__annotations__ == {'a_id': 'str', 'b': 'Union[str, StubCyclicB]'}
    assert rt.stubs.StubCyclicB.__annotations__ == {'b_id': 'str', 'a': 'Union[str, StubCyclicA]'}


if __name__ == '__main__':
    pytest.main([__file__])
