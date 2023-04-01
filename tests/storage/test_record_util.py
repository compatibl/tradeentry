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

SIMPLE_PK = 'rt.Type1;A;B'
SIMPLE_TOKENS = ['rt.Type1', 'A', 'B']
COMPOSITE_PK = 'rt.Type2;{rt.Type1;A;B};C'
COMPOSITE_TOKENS = ['rt.Type2', SIMPLE_PK, 'C']
MULTI_LEVEL_PK = 'rt.Type3;{rt.Type2;{rt.Type1;A;B};C};D'
MULTI_LEVEL_TOKENS = ['rt.Type3', COMPOSITE_PK, 'D']


class TestRecordUtil:
    """Tests for RecordUtil class."""

    def test_composite_pk(self):
        """Test test_composite_pk(...) function."""

        assert rt.RecordUtil.composite_pk(*SIMPLE_TOKENS) == SIMPLE_PK
        assert rt.RecordUtil.composite_pk(*COMPOSITE_TOKENS) == COMPOSITE_PK
        assert rt.RecordUtil.composite_pk(*MULTI_LEVEL_TOKENS) == MULTI_LEVEL_PK

    def test_split_simple_pk(self):
        """Test split_simple_pk(...) function."""

        assert rt.RecordUtil.split_simple_pk(SIMPLE_PK) == SIMPLE_TOKENS

        # This should not work
        with pytest.raises(Exception):
            rt.RecordUtil.split_simple_pk(COMPOSITE_PK)

    def test_split_composite_pk(self):
        """Test split_composite_pk(...) function."""

        assert rt.RecordUtil.split_composite_pk(SIMPLE_PK) == SIMPLE_TOKENS
        assert rt.RecordUtil.split_composite_pk(COMPOSITE_PK) == COMPOSITE_TOKENS
        assert rt.RecordUtil.split_composite_pk(MULTI_LEVEL_PK) == MULTI_LEVEL_TOKENS


if __name__ == '__main__':
    pytest.main([__file__])
