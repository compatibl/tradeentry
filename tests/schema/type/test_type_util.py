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

from cl.runtime.core.storage.deleted_record import DeletedRecord
from cl.runtime.core.schema.type.type_util import TypeUtil
from cl.runtime.stubs.storage.stub_class_data import StubClassData
from cl.runtime.stubs.storage.stub_class_record_key import StubClassRecordKey
from cl.runtime.stubs.storage.stub_class_record import StubClassRecord
from cl.runtime.stubs.storage.stub_derived_class_data import StubDerivedClassData
from cl.runtime.stubs.storage.stub_derived_class_record import StubDerivedClassRecord


class TestTypeUtil:
    """Tests for TypeUtil."""

    def test_get_type(self):
        """Test getting type from _t discriminators."""

        # from cl.runtime.stubs.storage.stub_class_record import StubClassRecord
        # from cl.runtime.stubs.storage.stub_derived_class_record import StubDerivedClassRecord

        with pytest.raises(Exception):
            TypeUtil.get_type('TypeUtil')
        with pytest.raises(Exception):
            TypeUtil.get_type('Record')

        # Returns type from name
        assert TypeUtil.get_type('StubClassRecord') == StubClassRecord
        assert TypeUtil.get_type('StubDerivedClassRecord') == StubDerivedClassRecord
        assert TypeUtil.get_type('StubClassData') == StubClassData
        assert TypeUtil.get_type('StubDerivedClassData') == StubDerivedClassData

        # Check that caching the results works by calling again with the same inputs
        assert TypeUtil.get_type('StubClassRecord') == StubClassRecord

    def test_get_ultimate_base(self):
        """Smoke test."""

        with pytest.raises(Exception):
            TypeUtil.get_ultimate_base(TypeUtil)

        # Check results
        assert TypeUtil.get_ultimate_base(StubClassRecord) == StubClassRecord
        assert TypeUtil.get_ultimate_base(StubDerivedClassRecord) == StubClassRecord
        assert TypeUtil.get_ultimate_base(StubClassData) == StubClassData

        # Check that caching the results works by calling again with the same inputs
        assert TypeUtil.get_ultimate_base(StubClassRecord) == StubClassRecord

    def test_hierarchical_discriminator(self):
        """Test hierarchical discriminator."""
        func = TypeUtil.get_hierarchical_discriminator

        # Must return the list of classes from current to the first user-defined base
        assert func(StubClassRecord) == ['StubClassRecord']
        assert func(StubDerivedClassRecord) == ['StubClassRecord', 'StubDerivedClassRecord']
        assert func(StubClassData) == ['StubClassData']
        assert func(StubDerivedClassData) == ['StubClassData', 'StubDerivedClassData']
        assert func(StubClassRecordKey) == ['StubClassRecordKey']
        assert func(DeletedRecord) == ['DeletedRecord']

        # Check that caching the results works by calling again with the same inputs
        assert func(StubClassRecord) == ['StubClassRecord']

    def test_key_from_record(self):
        """Test getting key class from record class."""

        func = TypeUtil.get_key_from_record

        # Must return base key from base or derived record
        assert func(StubClassRecord) == StubClassRecordKey
        assert func(StubDerivedClassRecord) == StubClassRecordKey

        # Check that caching the results works by calling again with the same inputs
        assert func(StubClassRecord) == StubClassRecordKey

    def test_record_from_key(self):
        """Test getting base record from key."""

        func = TypeUtil.get_record_from_key

        # Must return base record from key
        assert func(StubClassRecordKey) == StubClassRecord

        # Check that caching the results works by calling again with the same inputs
        assert func(StubClassRecordKey) == StubClassRecord

    def test_package_shortname(self):
        """Test short package namespace alias."""

        assert TypeUtil.try_get_type('rt.stubs.StubClassRecord') is None
        assert TypeUtil.try_get_type('rt.stubs.StubDerivedClassRecord') is None

        assert TypeUtil.get_prefixed_name(StubClassRecord) == 'StubClassRecord'
        assert TypeUtil.get_prefixed_name(StubDerivedClassRecord) == 'StubDerivedClassRecord'

        # Add package shortname
        TypeUtil.register_shortname('cl.runtime.stubs', 'rt.stubs')

        assert TypeUtil.get_type('rt.stubs.StubClassRecord') is StubClassRecord
        assert TypeUtil.get_type('rt.stubs.StubDerivedClassRecord') is StubDerivedClassRecord

        assert TypeUtil.get_prefixed_name(StubClassRecord) == 'rt.stubs.StubClassRecord'
        assert TypeUtil.get_prefixed_name(StubDerivedClassRecord) == 'rt.stubs.StubDerivedClassRecord'

        assert TypeUtil.get_collection_name(StubClassRecord) == 'rt.stubs.StubClassRecord'
        assert TypeUtil.get_collection_name(StubDerivedClassRecord) == 'rt.stubs.StubClassRecord'

        func = TypeUtil.get_hierarchical_discriminator

        assert func(StubClassRecord) == ['rt.stubs.StubClassRecord']
        assert func(StubDerivedClassRecord) == ['rt.stubs.StubClassRecord', 'rt.stubs.StubDerivedClassRecord']
        assert func(StubClassData) == ['rt.stubs.StubClassData']
        assert func(StubDerivedClassData) == [
            'rt.stubs.StubClassData',
            'rt.stubs.StubDerivedClassData',
        ]
        assert func(StubClassRecordKey) == ['rt.stubs.StubClassRecordKey']
        assert func(DeletedRecord) == ['DeletedRecord']

        TypeUtil.unregister_shortname('cl.runtime.stubs')  # TODO: rename to deregister?


if __name__ == '__main__':
    pytest.main([__file__])
