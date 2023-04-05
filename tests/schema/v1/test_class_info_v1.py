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
from cl.runtime.core.schema.v1.class_info import ClassInfo
from cl.runtime.stubs.storage.stub_class_data import StubClassData
from cl.runtime.stubs.storage.stub_class_record_key import StubClassRecordKey
from cl.runtime.stubs.storage.stub_class_record import StubClassRecord
from cl.runtime.stubs.storage.stub_derived_class_data import StubDerivedClassData
from cl.runtime.stubs.storage.stub_derived_class_record import StubDerivedClassRecord


class TestClassInfo:
    """Tests for ClassInfo."""

    def test_get_type(self):
        """Test getting type from _t discriminators."""

        # from cl.runtime.stubs.storage.stub_class_record import StubClassRecord
        # from cl.runtime.stubs.storage.stub_derived_class_record import StubDerivedClassRecord

        with pytest.raises(Exception):
            ClassInfo.get_type('ClassInfo')
        with pytest.raises(Exception):
            ClassInfo.get_type('Record')

        assert ClassInfo.get_type('StubClassRecord') == StubClassRecord
        assert ClassInfo.get_type('StubDerivedClassRecord') == StubDerivedClassRecord
        assert ClassInfo.get_type('StubClassData') == StubClassData
        assert ClassInfo.get_type('StubDerivedClassData') == StubDerivedClassData

    def test_get_ultimate_base(self):
        """Smoke test."""

        with pytest.raises(Exception):
            ClassInfo.get_ultimate_base(ClassInfo)

        assert ClassInfo.get_ultimate_base(StubClassRecord) == StubClassRecord
        assert ClassInfo.get_ultimate_base(StubDerivedClassRecord) == StubClassRecord
        assert ClassInfo.get_ultimate_base(StubClassData) == StubClassData

    def test_hierarchical_discriminator(self):
        """Test hierarchical discriminator."""
        func = ClassInfo.get_hierarchical_discriminator

        # Must return the list of classes from current to the first user-defined base
        assert func(StubClassRecord) == ['StubClassRecord']
        assert func(StubDerivedClassRecord) == ['StubClassRecord', 'StubDerivedClassRecord']
        assert func(StubClassData) == ['StubClassData']
        assert func(StubDerivedClassData) == ['StubClassData', 'StubDerivedClassData']
        assert func(StubClassRecordKey) == ['StubClassRecordKey']
        assert func(DeletedRecord) == ['DeletedRecord']

    def test_key_from_record(self):
        """Test getting key class from record class."""

        func = ClassInfo.get_key_from_record

        # Must return base key from base or derived record
        assert func(StubClassRecord) == StubClassRecordKey
        assert func(StubDerivedClassRecord) == StubClassRecordKey

    def test_record_from_key(self):
        """Test getting base record from key."""

        func = ClassInfo.get_record_from_key

        # Must return base record from key
        assert func(StubClassRecordKey) == StubClassRecord

    def test_package_shortname(self):
        """Test short package namespace alias."""

        assert ClassInfo.try_get_type('rt.stubs.StubClassRecord') is None
        assert ClassInfo.try_get_type('rt.stubs.StubDerivedClassRecord') is None

        assert ClassInfo.get_prefixed_name(StubClassRecord) == 'StubClassRecord'
        assert ClassInfo.get_prefixed_name(StubDerivedClassRecord) == 'StubDerivedClassRecord'

        # Add package shortname
        ClassInfo.register_shortname('cl.runtime.stubs', 'rt.stubs')

        assert ClassInfo.get_type('rt.stubs.StubClassRecord') is StubClassRecord
        assert ClassInfo.get_type('rt.stubs.StubDerivedClassRecord') is StubDerivedClassRecord

        assert ClassInfo.get_prefixed_name(StubClassRecord) == 'rt.stubs.StubClassRecord'
        assert ClassInfo.get_prefixed_name(StubDerivedClassRecord) == 'rt.stubs.StubDerivedClassRecord'

        assert ClassInfo.get_collection_name(StubClassRecord) == 'rt.stubs.StubClassRecord'
        assert ClassInfo.get_collection_name(StubDerivedClassRecord) == 'rt.stubs.StubDerivedClassRecord'

        func = ClassInfo.get_hierarchical_discriminator

        assert func(StubClassRecord) == ['rt.stubs.StubClassRecord']
        assert func(StubDerivedClassRecord) == ['rt.stubs.StubClassRecord', 'rt.stubs.StubDerivedClassRecord']
        assert func(StubClassData) == ['rt.stubs.StubClassData']
        assert func(StubDerivedClassData) == [
            'rt.stubs.StubClassData',
            'rt.stubs.StubDerivedClassData',
        ]
        assert func(StubClassRecordKey) == ['rt.stubs.StubClassRecordKey']
        assert func(DeletedRecord) == ['DeletedRecord']

        ClassInfo.unregister_shortname('cl.runtime.stubs')  # TODO: rename to deregister?


if __name__ == '__main__':
    pytest.main([__file__])
