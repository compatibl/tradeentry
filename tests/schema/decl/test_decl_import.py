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

import cl.runtime.core.schema.v1.atomic_type
import cl.runtime.core.schema.v1.element_modification_type
import cl.runtime.core.schema.v1.enum_decl
import cl.runtime.core.schema.v1.enum_decl_key
import cl.runtime.core.schema.v1.enum_item_decl
import cl.runtime.core.schema.v1.handler_declare_block_decl
import cl.runtime.core.schema.v1.handler_declare_decl
import cl.runtime.core.schema.v1.handler_implement_block_decl
import cl.runtime.core.schema.v1.handler_implement_decl
import cl.runtime.core.schema.v1.handler_param_decl
import cl.runtime.core.schema.v1.handler_type
import cl.runtime.core.schema.v1.handler_variable_decl
import cl.runtime.core.schema.v1.index_decl
import cl.runtime.core.schema.v1.index_sort_order_enum
import cl.runtime.core.schema.v1.interface_decl
import cl.runtime.core.schema.v1.interface_decl_key
import cl.runtime.core.schema.v1.interface_implement_decl
import cl.runtime.core.schema.v1.language
import cl.runtime.core.schema.v1.language_key
import cl.runtime.core.schema.v1.module
import cl.runtime.core.schema.v1.module_key
import cl.runtime.core.schema.v1.package
import cl.runtime.core.schema.v1.package_dependency
import cl.runtime.core.schema.v1.package_key
import cl.runtime.core.schema.v1.type_argument_decl
import cl.runtime.core.schema.v1.type_decl
import cl.runtime.core.schema.v1.type_decl_key
import cl.runtime.core.schema.v1.type_element_decl
import cl.runtime.core.schema.v1.type_index_decl
import cl.runtime.core.schema.v1.type_kind
import cl.runtime.core.schema.v1.type_member_decl
import cl.runtime.core.schema.v1.type_param_constraint_type
import cl.runtime.core.schema.v1.type_param_decl
import cl.runtime.core.schema.v1.value_decl


def test_import():
    """Test import of schema declarations in v1 format."""

    # The test itself is no-op as it is only checking the import
    pass
