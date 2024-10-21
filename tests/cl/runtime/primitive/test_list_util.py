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
from cl.runtime.primitive.list_util import ListUtil


def test_is_empty():
    """Smoke test for functions in CaseUtil."""
    assert ListUtil.is_empty(None)
    assert ListUtil.is_empty([])
    assert not ListUtil.is_empty([1])


if __name__ == "__main__":
    pytest.main([__file__])
