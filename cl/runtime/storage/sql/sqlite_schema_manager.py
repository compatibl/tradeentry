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
from typing import Type, Dict, Iterable, cast

from cl.runtime.records.protocols import KeyProtocol, is_key, RecordProtocol


def get_key_class(type_: Type) -> Type[KeyProtocol]:
    """Get key class for given type."""

    for type_ in type_.__mro__:
        if is_key(type_):
            return cast(KeyProtocol, type_)

    raise RuntimeError(f'Not found key class for type {type_}.')


def _collect_all_classes_in_hierarchy(type_: Type[KeyProtocol]) -> Iterable[RecordProtocol]:
    """Collect all subtypes for given key class."""

    for subclass in type_.__subclasses__():
        subclass = cast(RecordProtocol, subclass)
        yield from _collect_all_classes_in_hierarchy(subclass)
        yield subclass


def _resolve_columns_for_type(type_: Type):
    """Collect all types in hierarchy and check type conflicts for fields with the same name."""


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
