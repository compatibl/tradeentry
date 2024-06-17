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
from cl.runtime.schema.schema import Schema
from cl.runtime.schema.type_decl import TypeDecl
from stubs.cl.runtime import StubDataclassRecord


def test_get_types():
    """Test Schema.get_types() method."""

    type_dict = Schema.get_type_dict()
    assert "TypeDecl" in type_dict
    assert "StubDataclassRecord" in type_dict
    assert "RecordMixin" not in type_dict


def test_get_type_by_short_name():
    """Test Schema.get_type_by_short_name() method."""

    assert Schema.get_type_by_short_name("TypeDecl") is TypeDecl
    assert Schema.get_type_by_short_name("StubDataclassRecord") is StubDataclassRecord


def test_get_type_by_class_path():
    """Test Schema.get_type_by_class_path() method."""

    assert Schema.get_type_by_class_path("cl.runtime.schema.type_decl.TypeDecl") is TypeDecl
    assert Schema.get_type_by_class_path(
        "stubs.cl.runtime.records.dataclasses.stub_dataclass_record.StubDataclassRecord"
    ) is StubDataclassRecord


if __name__ == "__main__":
    pytest.main([__file__])
