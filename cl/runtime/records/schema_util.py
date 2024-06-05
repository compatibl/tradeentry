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

import ast
import inspect
import textwrap
from typing import List
from typing import Type

from cl.runtime.schema.display_kind import DisplayKind
from cl.runtime.schema.module_decl import ModuleDecl
from cl.runtime.schema.type_decl import TypeDecl


class SchemaUtil:
    """Helper class for generating the schema."""

    @staticmethod
    def get_type_decl(record_type: Type) -> TypeDecl:
        """
        Get type declaration without the data specific to the dataclass framework. Use specialized
        helper classes for each dataclass framework to get complete type declarations.
        """

        module = ModuleDecl(module_path=record_type.__module__)
        key_fields = SchemaUtil.get_key_fields(record_type)

        elements = []

        result = TypeDecl(
            module=module.get_key(),
            name=record_type.__name__,
            comment=record_type.__doc__ or "",
            display_kind=DisplayKind.Basic,
            elements=elements,
            keys=key_fields
        )
        return result

    @staticmethod
    def get_key_fields(record_type: Type) -> List[str]:
        """
        Get key fields by parsing the source of 'get_key' method.

        Notes:
            This method parses the source code of 'get_key' method and returns all instance
            fields it accesses in the order of access, for example if 'get_key' source is:

            def get_key(self) -> Tuple[Type, str, int]:
                return ClassName, self.key_field_1, self.key_field_2

            this method will return:

            ["key_field_1", "key_field_2"]
        """

        # Get source code for the 'get_key' method
        if hasattr(record_type, "get_key"):
            get_key_source = inspect.getsource(record_type.get_key)
        else:
            raise RuntimeError(
                f"Cannot get key fields because {record_type.__name__} " f"does not implement 'get_key' method."
            )

        # Because 'ast' expects the code to be correct as though it is at top level,
        # remove excess indent from the source to make it suitable for parsing
        get_key_source = textwrap.dedent(get_key_source)

        # Extract field names from the AST of 'get_key' method
        get_key_ast = ast.parse(get_key_source)
        key_fields = []
        for node in ast.walk(get_key_ast):
            # Find every instance field of 'cls' accessed inside the source of 'get_key' method.
            # Accumulate in list in the order they are accessed
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":
                key_fields.append(node.attr)

        return key_fields
