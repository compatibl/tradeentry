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
import cl.runtime_samples as samples


class TestDataClassRecord:
    """Tests for DataClassRecord class."""

    def test_smoke(self):
        """Smoke test."""

        context = rt.Context()

        record = samples.DataClassRecordSample()
        record.context = context
        record.primary_key_field_str = 'abc'
        record.primary_key_field_int = 123
        record.base_record_field_str = 'def'
        record.base_record_field_float = 4.56

        # Test that context has been set
        assert record.context == context

        # Test primary key
        pk = record.to_pk()
        assert pk == 'samples.DataClassRecordSample;abc;123'


if __name__ == '__main__':
    pytest.main([__file__])
