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
from stubs.cl.runtime.storage.attrs.stub_attrs_data import StubAttrsData
from stubs.cl.runtime.storage.attrs.stub_attrs_record_key import StubAttrsRecordKey
from stubs.cl.runtime.storage.attrs.stub_attrs_record import StubAttrsRecord
from stubs.cl.runtime.storage.attrs.stub_attrs_derived_record import StubAttrsDerivedRecord


def test_get_class_path():
    """Test getting class path from class."""

    # Base class
    base_path = f"{StubAttrsRecord.__module__}.{StubAttrsRecord.__name__}"
    assert rt.RecordUtil.get_class_path(StubAttrsRecord) == base_path

    # Derived class
    derived_path = f"{StubAttrsDerivedRecord.__module__}.{StubAttrsDerivedRecord.__name__}"
    assert rt.RecordUtil.get_class_path(StubAttrsDerivedRecord) == derived_path


def test_split_class_path():
    """Test splitting class path into module and class name."""

    # Base class
    base_path = f"{StubAttrsRecord.__module__}.{StubAttrsRecord.__name__}"
    base_result = StubAttrsRecord.__module__, StubAttrsRecord.__name__
    assert rt.RecordUtil.split_class_path(base_path) == base_result

    # Derived class
    derived_path = f"{StubAttrsDerivedRecord.__module__}.{StubAttrsDerivedRecord.__name__}"
    derived_result = StubAttrsDerivedRecord.__module__, StubAttrsDerivedRecord.__name__
    assert rt.RecordUtil.split_class_path(derived_path) == derived_result


def test_get_class_type():
    """Test getting class from module and class strings."""

    # Class that is already imported
    assert rt.RecordUtil.get_class_type(rt.RecordUtil.__module__, rt.RecordUtil.__name__) == rt.RecordUtil

    # Class that is dynamically imported on demand
    do_no_import_module_name = "stubs.cl.runtime.storage.attrs.stub_attrs_do_not_import"
    do_no_import_class_name = "StubAttrsDoNotImport"
    do_no_import_class = rt.RecordUtil.get_class_type(do_no_import_module_name, do_no_import_class_name)
    assert do_no_import_class.__module__ == do_no_import_module_name
    assert do_no_import_class.__name__ == do_no_import_class_name

    # Module does not exist error
    unknown_name = "aBcDeF"
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_class_type(unknown_name, do_no_import_class_name)

    # Class does not exist error
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_class_type(do_no_import_module_name, unknown_name)

    # Dot-delimited class name error
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_class_type(do_no_import_module_name, "a.b")

    # Call one more time and confirm that method results are cached
    assert rt.RecordUtil.get_class_type(rt.RecordUtil.__module__, rt.RecordUtil.__name__) == rt.RecordUtil
    assert rt.RecordUtil.get_class_type.cache_info().hits > 0


def test_get_inheritance_chain():
    """Test getting class path from class."""

    key_class = "StubAttrsRecordKey"
    base_class = "StubAttrsRecord"
    derived_class = "StubAttrsDerivedRecord"

    # Key class, returns self
    assert rt.RecordUtil.get_inheritance_chain(StubAttrsRecordKey) == [key_class]

    # Common base class, returns self and key class
    assert rt.RecordUtil.get_inheritance_chain(StubAttrsRecord) == [base_class, key_class]

    # Derived class, returns self, common base and key
    assert rt.RecordUtil.get_inheritance_chain(StubAttrsDerivedRecord) == [derived_class, base_class, key_class]

    # Invoke for a type that does not have a key class
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_inheritance_chain(StubAttrsData)

    # Call one more time and confirm that method results are cached
    assert rt.RecordUtil.get_inheritance_chain(StubAttrsRecord) == [base_class, key_class]
    assert rt.RecordUtil.get_inheritance_chain.cache_info().hits > 0


def test_get_table():
    """Test getting table name from class."""

    # Key class
    assert rt.RecordUtil.get_table(StubAttrsRecordKey) == "StubAttrsRecord"

    # Common base class
    assert rt.RecordUtil.get_table(StubAttrsRecord) == "StubAttrsRecord"

    # Derived class
    assert rt.RecordUtil.get_table(StubAttrsDerivedRecord) == "StubAttrsRecord"

    # Error if a type does not have key class
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_table(StubAttrsData)

    # Call one more time and confirm that method results are cached
    assert rt.RecordUtil.get_table(StubAttrsRecordKey) == "StubAttrsRecord"
    assert rt.RecordUtil.get_table.cache_info().hits > 0


def test_to_from_dict():
    """Test dictionary serialization roundtrip."""

    # List of types for which serialization will be tested
    stub_types = [StubAttrsData, StubAttrsRecord]

    for stub_type in stub_types:

        # Create a stub type instance with default field values
        obj = stub_type()

        # Serialize to dict
        data = rt.RecordUtil.to_dict(obj)

        # Restore from dict
        restored_obj = rt.RecordUtil.from_dict(stub_type, data)

        # Compare
        assert obj == restored_obj




if __name__ == '__main__':
    pytest.main([__file__])
