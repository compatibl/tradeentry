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
from cl.runtime.records.key_util import KeyUtil
from cl.runtime.schema.module_decl import ModuleDecl
from cl.runtime.schema.module_decl_key import ModuleDeclTable
from cl.runtime.schema.type_decl import TypeDecl
from cl.runtime.schema.type_decl_key import TypeDeclKey, TypeDeclTable


def test_to_dict():
    """Test KeyUtil.to_dict method."""

    key = TypeDeclTable, (ModuleDeclTable, "class_module"), "ClassName"
    result = KeyUtil.to_dict(key)  # TODO: Fix type error
    assert result == {"module": {"module_name": "class_module"}, "name": "ClassName"}


def test_parse_key():
    """Test KeyUtil.parse_key method."""

    key = TypeDeclTable, (ModuleDeclTable, "module"), "ClassName"
    result = KeyUtil.parse_key(TypeDeclKey, key)

    _, (_, x), y = key

    # TODO: Add check
    pass


def test_get_key_fields():
    """Test KeyUtil.get_key_fields method."""

    assert KeyUtil.get_key_fields(TypeDecl) == ["module", "name"]
    assert KeyUtil.get_key_fields(ModuleDecl) == ["module_name"]


if __name__ == "__main__":
    pytest.main([__file__])
