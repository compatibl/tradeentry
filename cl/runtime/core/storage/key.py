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

from abc import ABC, abstractmethod


class Key(ABC):
    """
    Abstract base class that provides logical table name and primary key for records that can be stored in a
    document or relational database, key-value store, cloud bucket store, or filesystem.

    Derived classes must implement the following methods:

    - get_record_class() - Return root of the record class hierarchy for which this key is defined.
    - get_table() - Return table name as dot-delimited string. Physical table name in storage may differ.
    - get_pk() - Return primary key as semicolon-delimited string. Physical primary key in storage may differ.
    """

    @abstractmethod
    def get_table_name(self) -> str:
        """Return unique table name as plain or dot-delimited string according to the user-specified convention.

        The recommended convention is to use the result of `get_type_name` for the root class of the
        class hierarchy stored in the database table. However, any other plain or dot-delimited string
        can be used as long as it is unique across all imported modules.

        Examples:

            - `rt.DataSource` and `rt.stubs.StubRecord`
            - `cl.runtime.DataSource` and `cl.runtime.stubs.StubRecord`
            - `DataSource` and `StubRecord` (if class names are unique across all imported modules)

        Notes:

            Table name in physical storage or cache may not match this logical table name format.
            The conversion is performed by the data source implementation.
        """

    @abstractmethod
    def get_pk(self) -> str:
        """Return logical primary key (PK) as string in semicolon-delimited format.

        For composite keys, the embedded keys are concatenated in the
        order of their declaration without brackets.

        Examples:

            - One primary key field A: `pk=A`
            - Two primary key fields A and B: `pk=A;B`
            - Two primary key fields, first field is composite key`A1;A2` and second is B: `pk=A1;A2;B`

        Notes:

            Primary key in physical storage or cache may not match this logical primary key format.
            The conversion is performed by the data source implementation.
        """

    def __str__(self) -> str:
        """Return primary key by default. Derived classes may override to provide more information.

        Notes:

            Conversion to string is provided for debugging purposes only and may be modified in derived
            classes. Data source implementation must use `get_pk` method instead.
        """
        return self.get_pk()
