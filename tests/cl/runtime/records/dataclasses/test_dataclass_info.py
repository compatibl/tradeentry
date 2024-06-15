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
from cl.runtime import ClassInfo
from stubs.cl.runtime import StubDataclassCyclicA
from stubs.cl.runtime import StubDataclassCyclicB
from stubs.cl.runtime import StubDataclassData
from stubs.cl.runtime import StubDataclassDerivedData
from stubs.cl.runtime import StubDataclassDerivedFromDerivedData
from stubs.cl.runtime import StubDataclassDerivedFromDerivedRecord
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassDictFields
from stubs.cl.runtime import StubDataclassDictListFields
from stubs.cl.runtime import StubDataclassDoNotImport
from stubs.cl.runtime import StubDataclassListDictFields
from stubs.cl.runtime import StubDataclassListFields
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassOtherDerivedRecord
from stubs.cl.runtime import StubDataclassPrimitiveFields
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime import StubDataclassRecordKey
from stubs.cl.runtime import StubDataclassSingleton


def test_get_class_path():
    """Test getting class path from class."""

    # Base class
    base_path = f"{StubDataclassRecord.__module__}.{StubDataclassRecord.__name__}"
    assert ClassInfo.get_class_path(StubDataclassRecord) == base_path

    # Derived class
    derived_path = f"{StubDataclassDerivedRecord.__module__}.{StubDataclassDerivedRecord.__name__}"
    assert ClassInfo.get_class_path(StubDataclassDerivedRecord) == derived_path


def test_split_class_path():
    """Test splitting class path into module and class name."""

    # Base class
    base_path = f"{StubDataclassRecord.__module__}.{StubDataclassRecord.__name__}"
    base_result = StubDataclassRecord.__module__, StubDataclassRecord.__name__
    assert ClassInfo.split_class_path(base_path) == base_result

    # Derived class
    derived_path = f"{StubDataclassDerivedRecord.__module__}.{StubDataclassDerivedRecord.__name__}"
    derived_result = StubDataclassDerivedRecord.__module__, StubDataclassDerivedRecord.__name__
    assert ClassInfo.split_class_path(derived_path) == derived_result


def test_get_class_type():
    """Test getting class from module and class strings."""

    # Class that is already imported
    class_info_path = f"{ClassInfo.__module__}.{ClassInfo.__name__}"
    assert ClassInfo.get_class_type(class_info_path) == ClassInfo

    # Class that is dynamically imported on demand
    do_no_import_class_path = (
        "stubs.cl.runtime.records.dataclasses.stub_dataclass_do_not_import.StubDataclassDoNotImport"
    )
    do_no_import_class = ClassInfo.get_class_type(do_no_import_class_path)
    assert do_no_import_class_path == f"{do_no_import_class.__module__}.{do_no_import_class.__name__}"

    # Module does not exist error
    unknown_name = "aBcDeF"
    with pytest.raises(RuntimeError):
        path_with_unknown_module = "unknown_module.StubDataclassDoNotImport"
        ClassInfo.get_class_type(path_with_unknown_module)

    # Class does not exist error
    with pytest.raises(RuntimeError):
        path_with_unknown_class = "stubs.cl.runtime.records.dataclasses.stub_dataclass_do_not_import.UnknownClass"
        ClassInfo.get_class_type(path_with_unknown_class)

    # Call one more time and confirm that method results are cached
    assert ClassInfo.get_class_type(class_info_path) == ClassInfo
    assert ClassInfo.get_class_type.cache_info().hits > 0


def test_get_inheritance_chain():
    """Test getting class path from class."""

    base_class = "StubDataclassRecord"
    derived_class = "StubDataclassDerivedRecord"

    # Common base class, returns self and key class
    assert ClassInfo.get_inheritance_chain(StubDataclassRecord) == [base_class]

    # Derived class, returns self, common base and key
    assert ClassInfo.get_inheritance_chain(StubDataclassDerivedRecord) == [derived_class, base_class]

    # Invoke for a type that does not have a key class
    with pytest.raises(RuntimeError):
        ClassInfo.get_inheritance_chain(StubDataclassData)

    # Call one more time and confirm that method results are cached
    assert ClassInfo.get_inheritance_chain(StubDataclassRecord) == [base_class]
    assert ClassInfo.get_inheritance_chain.cache_info().hits > 0


def test_to_from_dict():
    """Test dictionary serialization roundtrip."""

    # List of types for which serialization will be tested
    # TODO: Support remaining classes
    stub_types = [
        # StubDataclassCyclicA,
        # StubDataclassCyclicB,
        StubDataclassRecord,
        # StubDataclassDerivedFromDerivedRecord,
        # StubDataclassDerivedRecord,
        # StubDataclassDictFields,
        # StubDataclassDictListFields,
        # StubDataclassDoNotImport,
        # StubDataclassListDictFields,
        # StubDataclassListFields,
        # StubDataclassNestedFields,
        # StubDataclassOtherDerivedRecord,
        # StubDataclassPrimitiveFields,
        # StubDataclassSingleton,
    ]

    for stub_type in stub_types:
        # Create a stub type instance with default field values
        record = stub_type()
        key = record.get_key()
        packed_key, (packed_type, packed_dict) = record.pack()
        assert packed_key == key

        # Restore from dict
        record_clone = stub_type(**packed_dict)  # noqa
        clone_key, (clone_type, clone_dict) = record_clone.pack()

        # Compare
        assert clone_key == key
        assert clone_type == packed_type
        assert clone_dict == packed_dict
        assert record_clone == record


if __name__ == "__main__":
    pytest.main([__file__])
