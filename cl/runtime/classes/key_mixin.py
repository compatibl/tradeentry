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

from __future__ import annotations

from abc import ABC
from typing import TypeVar, Type, Literal

from cl.runtime.classes.class_info import ClassInfo
from cl.runtime.classes.data_mixin import DataMixin

# Generic parameter for the key and record types
TKey = TypeVar('TKey', bound='KeyMixin', covariant=False, contravariant=False)
TRecordOrKey = TypeVar('TRecordOrKey', bound='KeyMixin', covariant=True, contravariant=False)

# Key format type
KeyFormat = Literal["record", "key", "dict", "str", "unknown"]


class KeyMixin(DataMixin, ABC):
    """
    Optional mixin class for database keys providing static type checkers with method signatures.

    Those methods that raise an exception must be overridden in derived types or by a decorator.
    They are not made abstract to avoid errors from static type checkers.

    The use of this class is optional. The code must not rely on inheritance from this class.
    """

    __slots__ = []  # Adding an empty __slots__ declaration prevents the creation of a __dict__ for every instance

    def get_table(self) -> str:
        """
        Name of the database table where the record for this key is stored.

        By convention, table name consists of a namespace (full package path or short alias)
        followed by the dot delimiter and then the class name of the common base to all records
        stored in the table: 'namespace.RecordType'
        """
        raise RuntimeError(
            f"Method get_table() for class {type(self).__name__} in module {type(self).__module__} "
            f"is neither implemented in code nor by a decorator."
        )

    @classmethod
    def to_generic_key(cls: Type[TRecordOrKey], record_or_key: TRecordOrKey | dict | str | None) -> str | None:
        """
        Generic key string defines both the table and the record within the table. It consists of the
        table name followed by the primary key in semicolon-delimited string format.

        By convention, table name consists of a namespace (full package path or short alias) followed by
        the class name of the common base to all classes stored in the table with dot delimiter:

        - No primary key fields: 'namespace.RecordType'
        - One primary key field A: 'namespace.RecordType;A'
        - Two primary key fields A and B: 'namespace.RecordType;A;B'
        - Two primary key fields 'A1;A2' and 'B': 'namespace.RecordType;A1;A2;B'
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        """
        Key as string in semicolon-delimited string format without table name.

        Notes:
            This method is for debugging purposes only and may be overridden in derived types. Do not use in code.
        """
        class_type = type(self)  # TODO: Support calling this method for types derived from key
        return ClassInfo.to_str_key(class_type, class_type, self)
