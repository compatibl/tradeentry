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
from typing_extensions import Self
from cl.runtime.schema.dataclasses.dataclass_field_decl import DataclassFieldDecl
from cl.runtime.schema.type_decl import TypeDecl
from cl.runtime.schema.element_decl import ElementDecl
from dataclasses import dataclass
from typing import get_type_hints, Type


@dataclass(slots=True, kw_only=True)
class DataclassTypeDecl(TypeDecl):
    """Type declaration for a dataclass."""

    @classmethod
    def create(cls, record_type: Type) -> Self:
        """Create type declaration for a dataclass."""

        if not dataclasses.is_dataclass(record_type):
            raise RuntimeError(f"Class {record_type.__name__} is not a dataclass.")

        # Create partial type declaration without elements
        result = cls._create_partial(record_type)

        # Information about dataclass fields including the metadata (does not resolve ForwardRefs)
        fields = dataclasses.fields(cls)

        # Get type hints to resolve ForwardRefs
        type_hints = get_type_hints(cls)

        # Add elements
        result.elements = []
        for field in fields:

            # Get type from type hints because they resolve forward references
            field_type = type_hints[field.name]

            # Get the rest of the data from the field itself
            field_decl = DataclassFieldDecl.create(field, field_type)

            # Convert to element and add
            element_decl = ElementDecl.create(field_decl)
            result.elements.append(element_decl)

        # Get key fields by parsing the source of 'get_key' method
        result.keys = DataclassTypeDecl._get_key_fields(record_type)

        return result
