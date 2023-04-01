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
import re

SIMPLE_PK = 'rt.SimpleKeyType;ABC;DEF'
SIMPLE_TOKENS = ['rt.SimpleKeyType', 'ABC', 'DEF']
COMPOSITE_PK = 'rt.CompositeKeyType;{rt.SimpleKeyType;ABC;DEF};GHI'
COMPOSITE_TOKENS = ['rt.CompositeKeyType', SIMPLE_PK, 'GHI']
MULTI_LEVEL_PK = 'rt.MultiLevelKeyType;{rt.CompositeKeyType;{rt.SimpleKeyType;ABC;DEF};GHI};JKL'
MULTI_LEVEL_TOKENS = ['rt.MultiLevelKeyType', COMPOSITE_PK, 'JKL']


class TestRecordUtil:
    """Tests for RecordUtil class."""

    def test_to_pk(self):
        """Test to_pk(...) function."""

        assert rt.RecordUtil.to_pk(SIMPLE_TOKENS[0], SIMPLE_TOKENS[1:]) == SIMPLE_PK
        assert rt.RecordUtil.to_pk(COMPOSITE_TOKENS[0], COMPOSITE_TOKENS[1:]) == COMPOSITE_PK
        assert rt.RecordUtil.to_pk(MULTI_LEVEL_TOKENS[0], MULTI_LEVEL_TOKENS[1:]) == MULTI_LEVEL_PK

    def test_from_pk(self):
        """Test to_pk(...) function."""

        assert rt.RecordUtil.split_pk(SIMPLE_PK) == SIMPLE_TOKENS
        assert rt.RecordUtil.split_pk(COMPOSITE_PK) == COMPOSITE_TOKENS
        assert rt.RecordUtil.split_pk(MULTI_LEVEL_PK) == MULTI_LEVEL_TOKENS


if __name__ == '__main__':
    pytest.main([__file__])
