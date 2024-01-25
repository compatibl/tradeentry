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

import cl.runtime.schema.decl.atomic_type
import cl.runtime.schema.decl.element_modification_type
import cl.runtime.schema.decl.enum_decl
import cl.runtime.schema.decl.enum_decl_key
import cl.runtime.schema.decl.enum_item_decl
import cl.runtime.schema.decl.handler_declare_block_decl
import cl.runtime.schema.decl.handler_declare_decl
import cl.runtime.schema.decl.handler_implement_block_decl
import cl.runtime.schema.decl.handler_implement_decl
import cl.runtime.schema.decl.handler_param_decl
import cl.runtime.schema.decl.handler_type
import cl.runtime.schema.decl.handler_variable_decl
import cl.runtime.schema.decl.index_decl
import cl.runtime.schema.decl.index_sort_order_enum
import cl.runtime.schema.decl.interface_decl
import cl.runtime.schema.decl.interface_decl_key
import cl.runtime.schema.decl.interface_implement_decl
import cl.runtime.schema.decl.language
import cl.runtime.schema.decl.language_key
import cl.runtime.schema.decl.module
import cl.runtime.schema.decl.module_key
import cl.runtime.schema.decl.package
import cl.runtime.schema.decl.package_dependency
import cl.runtime.schema.decl.package_key
import cl.runtime.schema.decl.type_argument_decl
import cl.runtime.schema.decl.type_decl
import cl.runtime.schema.decl.type_decl_key
import cl.runtime.schema.decl.type_element_decl
import cl.runtime.schema.decl.type_index_decl
import cl.runtime.schema.decl.type_kind
import cl.runtime.schema.decl.type_member_decl
import cl.runtime.schema.decl.type_param_constraint_type
import cl.runtime.schema.decl.type_param_decl
import cl.runtime.schema.decl.value_decl


def test_import():
    """Test import of declaration modules."""

    # TODO: The test itself is no-op as it is only checking Python module import
    pass
