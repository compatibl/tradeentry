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

import dataclasses
from cl.runtime.schema.dataclasses.dataclass_field_decl import DataclassFieldDecl
from cl.runtime.schema.element_decl import ElementDecl
from cl.runtime.schema.type_decl import TypeDecl
from cl.runtime.schema.type_decl import for_type_key_maker
from dataclasses import dataclass
from memoization import cached
from typing import Set
from typing import Type
from typing import get_type_hints
from typing_extensions import Self


@dataclass(slots=True, kw_only=True)
class DataclassTypeDecl(TypeDecl):
    """Type declaration for a dataclass."""

    @classmethod
    @cached(custom_key_maker=for_type_key_maker)
    def for_type(cls, record_type: Type, *, dependencies: Set[Type] | None = None, skip_fields: bool = False) -> Self:
        """
        Create or return cached object for the specified record type.

        Args:
            record_type: Type of the record for which the declaration is created
            dependencies: Set of types used in field or methods of the specified type, populated only if not None
            skip_fields: Use this flag to skip fields generation when the method is invoked from a derived class
        """

        if not dataclasses.is_dataclass(record_type):
            raise RuntimeError(f"DataclassTypeDecl used for {record_type.__name__} which is not a dataclass.")

        # Populate using TypeDecl base
        result = TypeDecl.for_type(record_type, dependencies=dependencies, skip_fields=True)

        # Use this flag to skip fields generation when the method is invoked from a derived class
        if not skip_fields:
            # Information about dataclass fields including the metadata (does not resolve ForwardRefs)
            fields = dataclasses.fields(record_type)

            # Get type hints to resolve ForwardRefs
            type_hints = get_type_hints(record_type)

            # Dictionary of member comments (docstrings), currently requires source parsing due Python limitations
            member_comments = cls.get_member_comments(record_type)

            # Add elements
            result.elements = []
            for field in fields:
                # Get type from type hints because they resolve forward references
                field_type = type_hints[field.name]

                # Field comment (docstring)
                field_comment = member_comments.get(field.name, None)

                # Get the rest of the data from the field itself
                field_decl = DataclassFieldDecl.create(record_type, field, field_type, field_comment)

                # Convert to element and add
                element_decl = ElementDecl.create(field_decl)
                result.elements.append(element_decl)

        return result
