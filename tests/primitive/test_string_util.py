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
from cl.runtime.core.primitive.string_util import to_pascal_case, to_snake_case


def test_functions():
    """Smoke test for functions in string_util."""

    assert 'AbcDef' == to_pascal_case('abc_def')
    assert 'Some2dPoint' == to_pascal_case('some2d_point')
    assert 'Great2DPicture' == to_pascal_case('great2_d_picture')

    assert 'abc_def' == to_snake_case('AbcDef')
    assert 'some2d_point' == to_snake_case('Some2dPoint')
    assert 'great2_d_picture' == to_snake_case('Great2DPicture')


if __name__ == '__main__':
    pytest.main([__file__])
