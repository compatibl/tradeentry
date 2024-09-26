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

import inspect
from dataclasses import Field
from dataclasses import dataclass
from typing import Type
from typing_extensions import Self
from cl.runtime.schema.field_decl import FieldDecl


@dataclass(slots=True, kw_only=True)
class DataclassFieldDecl(FieldDecl):
    """Field declaration for a dataclass type."""

    @classmethod
    def create(cls, record_type: Type, field: Field, field_type: Type, field_comment: str) -> Self:
        """
        Create from dataclass field definition and field_type obtained from get_type_hints.

        Notes:
            The Field object also contains the type but it is not resolved in case of ForwardRef.
            For this reason, field_type obtained from get_type_hints is used as well.

        Args:
            record_type: Type of the record for which the field is defined
            field: Dataclass field definition
            field_type: Type of the field obtained from get_type_hints where ForwardRefs are resolved
            field_comment: Field comment (docstring), currently requires source parsing due Python limitations
        """

        # Use base class to populate fields that do not require access to dataclasses metadata
        result = FieldDecl.create(record_type, field.name, field_type, field_comment)

        # Populate fields that require access to dataclasses metadata
        metadata = dict(field.metadata)
        if (name := metadata.pop("name", None)) is not None:
            result.name = name
        if (label := metadata.pop("label", None)) is not None:
            result.label = label
        if (formatter := metadata.pop("formatter", None)) is not None:
            result.formatter = formatter
        if (subtype := metadata.pop("subtype", None)) is not None:
            if subtype == "long":
                if result.field_type == "int":
                    result.field_type = "long"
                else:
                    raise RuntimeError(f"Subtype 'long' is not valid for field type {result.field_type}")
            else:
                raise RuntimeError(f"Subtype {subtype} is not recognized.")

        # Check that no parsed fields remained in metadata
        if len(metadata) > 0:
            raise RuntimeError(f"Unrecognized attributes in dataclass field metadata: {metadata.keys()}")

        return result
