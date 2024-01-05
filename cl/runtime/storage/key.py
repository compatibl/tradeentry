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
from typing import Any, Dict, Optional

from cl.runtime import Context
from cl.runtime.storage.data import Data


class Key(Data, ABC):
    """
    Abstract base class for database keys.

    Notes:
        The use of this class is optional. The code must not rely on inheritance from this class, but only on the
        presence of its methods. These methods may be implemented without using any specific base or mixin class.

        The methods that lack implementation must be overridden by a derived class in code or using a decorator.
        They are not made abstract to avoid errors from static type checkers in the latter case.
    """

    @classmethod
    def get_table(cls) -> str:
        """
        Name of the database table where data for this key is stored.

        Notes:
            By convention, table name consists of a namespace (full package path or short alias) followed by
            the class name of the common base to all classes stored in the table with dot delimiter.
        """
        raise RuntimeError(f"Class method {cls}.get_table() must be implemented in code or by a decorator.")

    def get_key(self) -> str:
        """
        Key as string in semicolon-delimited string format without table name.

        Notes:
            For composite keys, the embedded keys are concatenated in the order of their declaration without brackets:

            - No primary key fields: '' (i.e. empty string)
            - One primary key field A: 'A'
            - Two primary key fields A and B: 'A;B'
            - Two primary key fields 'A1;A2' and 'B': 'A1;A2;B'
        """
        raise RuntimeError(f"Method {type(self)}.get_key() must be implemented in code or by a decorator.")

    def init(self) -> None:
        """Validate dataclass attributes and use them to initialize object state."""
        raise RuntimeError(f"Method {type(self)}.init() must be implemented in code or by a decorator.")

    def get_generic_key(self) -> str:
        """
        Generic key string defines both the table and the record within the table. It consists of the
        table name followed by the primary key in semicolon-delimited string format.

        Notes:
            By convention, table name consists of a namespace (full package path or short alias) followed by
            the class name of the common base to all classes stored in the table with dot delimiter:

            - No primary key fields: 'package.MyClass'
            - One primary key field A: 'package.MyClass;A'
            - Two primary key fields A and B: 'package.MyClass;A;B'
            - Two primary key fields 'A1;A2' and 'B': 'package.MyClass;A1;A2;B'
        """
        return f"{self.get_table()};{self.get_key()}"

    def __str__(self) -> str:
        """
        Return key string without table by default. Derived classes may override to provide more information.

        Notes:
            This method is for debugging purposes only and may be modified to return different data.
            Data source implementation must use 'get_key' method instead.
        """
        return self.get_key()
