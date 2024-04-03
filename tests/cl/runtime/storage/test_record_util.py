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

    # Call again to test caching
    assert rt.RecordUtil.get_class_type(rt.RecordUtil.__module__, rt.RecordUtil.__name__) == rt.RecordUtil

    # Class that is dynamically imported on demand
    do_no_import_module_name = "stubs.cl.runtime.storage.attrs.stub_attrs_do_not_import"
    do_no_import_class_name = "StubAttrsDoNotImport"
    do_no_import_class = rt.RecordUtil.get_class_type(do_no_import_module_name, do_no_import_class_name)
    assert do_no_import_class.__module__ == do_no_import_module_name
    assert do_no_import_class.__name__ == do_no_import_class_name

    # Call again to test caching
    do_no_import_class = rt.RecordUtil.get_class_type(do_no_import_module_name, do_no_import_class_name)
    assert do_no_import_class.__module__ == do_no_import_module_name
    assert do_no_import_class.__name__ == do_no_import_class_name

    # Module does not exist error
    unknown_name = "aBcDeF"
    with pytest.raises(RuntimeError) as e:
        rt.RecordUtil.get_class_type(unknown_name, do_no_import_class_name)
    assert e.value.args[0] == f"Module {unknown_name} is not found when loading class {do_no_import_class_name}."

    # Class does not exist error
    with pytest.raises(RuntimeError) as e:
        rt.RecordUtil.get_class_type(do_no_import_module_name, unknown_name)
    assert e.value.args[0] == f"Module {do_no_import_module_name} does not contain top-level class {unknown_name}."

    # Dot-delimited class name error
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_class_type(do_no_import_module_name, "a.b")

    # Test caching of method results
    cache_info = rt.RecordUtil.get_class_type.cache_info()
    assert cache_info.hits == 2
    assert cache_info.misses == 5
    assert cache_info.current_size == 2


def test_get_inheritance_chain():
    """Test getting class path from class."""

    # Test helper method
    assert not rt.RecordUtil.is_init_implemented(rt.DataMixin)  # Not present
    assert not rt.RecordUtil.is_init_implemented(rt.RecordMixin)  # Abstract
    assert rt.RecordUtil.is_init_implemented(StubAttrsRecord)  # Implemented
    assert rt.RecordUtil.is_init_implemented(StubAttrsRecord)  # Implemented

    # Common base class, returns self (call twice to test caching)
    base_path = rt.RecordUtil.get_class_path(StubAttrsRecord)
    assert rt.RecordUtil.get_inheritance_chain(StubAttrsRecord) == [base_path]
    assert rt.RecordUtil.get_inheritance_chain(StubAttrsRecord) == [base_path]

    # Derived class, returns the root of hierarchy (call twice to test caching)
    derived_path = rt.RecordUtil.get_class_path(StubAttrsDerivedRecord)
    assert rt.RecordUtil.get_inheritance_chain(StubAttrsDerivedRecord) == [derived_path, base_path]
    assert rt.RecordUtil.get_inheritance_chain(StubAttrsDerivedRecord) == [derived_path, base_path]

    # Invoke for a type that does not implement get_table()
    # twice to test that caching does not fail on exception
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_inheritance_chain(StubAttrsData)
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_inheritance_chain(StubAttrsData)

    # Test caching of method results
    cache_info = rt.RecordUtil.get_inheritance_chain.cache_info()
    assert cache_info.hits == 2
    assert cache_info.misses == 4
    assert cache_info.current_size == 2


if __name__ == '__main__':
    pytest.main([__file__])
