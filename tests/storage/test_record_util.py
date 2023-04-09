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
from cl.runtime.core.storage.record_util import RecordUtil


def test_get_class():
    """Test getting class from module and class strings."""

    # Class that is already imported
    assert rt.RecordUtil.get_class(rt.RecordUtil.__module__, rt.RecordUtil.__name__) == rt.RecordUtil

    # Call again to test caching
    assert rt.RecordUtil.get_class(rt.RecordUtil.__module__, rt.RecordUtil.__name__) == rt.RecordUtil

    # Class that is dynamically imported on demand
    do_no_import_module_name = "cl.runtime.stubs.storage.stub_do_not_import"
    do_no_import_class_name = "StubDoNotImport"
    do_no_import_class = rt.RecordUtil.get_class(do_no_import_module_name, do_no_import_class_name)
    assert do_no_import_class.__module__ == do_no_import_module_name
    assert do_no_import_class.__name__ == do_no_import_class_name

    # Call again to test caching
    do_no_import_class = rt.RecordUtil.get_class(do_no_import_module_name, do_no_import_class_name)
    assert do_no_import_class.__module__ == do_no_import_module_name
    assert do_no_import_class.__name__ == do_no_import_class_name

    # Module does not exist error
    unknown_name = "aBcDeF"
    with pytest.raises(RuntimeError) as e:
        rt.RecordUtil.get_class(unknown_name, do_no_import_class_name)
    assert e.value.args[0] == f"Module {unknown_name} is not found when loading class {do_no_import_class_name}."

    # Class does not exist error
    with pytest.raises(RuntimeError) as e:
        rt.RecordUtil.get_class(do_no_import_module_name, unknown_name)
    assert e.value.args[0] == f"Module {do_no_import_module_name} does not contain top-level class {unknown_name}."

    # Dot-delimited class name error
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_class(do_no_import_module_name, "a.b")


def test_get_class_path():
    """Test getting class path from class."""

    class_path = f"{rt.RecordUtil.__module__}.{rt.RecordUtil.__name__}"
    assert rt.RecordUtil.get_class_path(rt.RecordUtil) == class_path


def test_get_inheritance_chain_paths():
    """Test getting class path from class."""

    root_path = RecordUtil.get_class_path(rt.stubs.StubClassRecord)
    derived_path = RecordUtil.get_class_path(rt.stubs.StubDerivedClassRecord)

    # Root class, returns self
    assert rt.RecordUtil.get_inheritance_chain_paths(rt.stubs.StubClassRecord) == [root_path]
    
    # Derived class, returns the root of hierarchy 
    assert rt.RecordUtil.get_inheritance_chain_paths(rt.stubs.StubDerivedClassRecord) == [derived_path, root_path]
    
    # Error, invoke for a type that does not implement get_root_class
    with pytest.raises(RuntimeError):
        rt.RecordUtil.get_inheritance_chain_paths(rt.stubs.StubClassRecordKey)


if __name__ == '__main__':
    pytest.main([__file__])
