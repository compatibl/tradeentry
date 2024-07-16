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

from dataclasses import dataclass
from typing import Type, List, Tuple, Dict

from inflection import camelize

from cl.runtime.schema.schema import Schema


def get_type_fields(type_: Type) -> Dict[str, Type]:
    """Return field name and type of annotation based type declaration."""
    return type_.__annotations__


def resolve_columns_for_type(type_: Type) -> List[str]:
    """Collect all types in hierarchy and check type conflicts for fields with the same name."""

    types_in_hierarchy = Schema.get_types_in_hierarchy(type_)

    # {field_name: (subclass_name, field_type)}
    all_fields: Dict[str, Tuple[str, Type]] = {}

    for type_ in types_in_hierarchy:

        fields = get_type_fields(type_).items()
        for field_name, field_type in fields:
            existing_field = all_fields.get(field_name)

            if existing_field is not None:
                # check if fields with the same name have compatible type
                if not issubclass(field_type, existing_field[1]):
                    raise TypeError(
                        f'Field {field_name}: {field_type} of class {type_.__name__} conflicts with the same field '
                        f'{field_name}: {existing_field[1]} in base class {existing_field[0]}'
                    )
            else:
                all_fields[field_name] = (type_.__name__, field_type)

    columns = [f'{class_name}.{camelize(field_name)}' for field_name, (class_name, _) in all_fields.items()]
    return columns


def create_table_for_type(type_: Type) -> None:
    """Create mile wide table for given type including columns for all parent and child types."""


@dataclass(slots=True, kw_only=True)
class SqlSchemaManager:

    def create_table(self, record_type: Type) -> None:
        """
        Create sqlite table for given type.

        Don`t need to specify column types because sqlite supports dynamic typing.
        Mile wide table contains columns for all subtypes.
        """
        if hasattr(record_type, "__slots__"):
            pass
