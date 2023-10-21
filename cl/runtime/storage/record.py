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


class Record(Data, ABC):
    """Abstract base class for records stored in a data source.

    The use of this class is optional. The code must not rely on inheritance from this class, but only on the
    presence of its methods. These methods may be implemented without using any specific base or mixin class.

    Final record classes stored in a data source must implement the following methods and properties.
    They may be provided by mixins and intermediate base classes using dataclass and similar frameworks.

    - context: Field or property with type Context that has both getter and setter.
    - get_common_base: Static method returning the type of the common base for all classes
      stored in the same table as this class.
    - get_key: Return primary key of this instance in semicolon-delimited string format.
      For example, key=`A;B` for a class with two primary key fields that have values `A` and `B`.
    - to_dict(self) - instance method serializing self as dictionary.
    - from_dict(self, data_dict) - instance method populating self from dictionary.
    """

    context: Optional[Context]
    """
    Context provides platform-independent APIs for:

    - Databases and distributed cache
    - Logging and error reporting
    - Local or remote handler execution
    - Progress reporting
    - Virtualized filesystem
    """

    def __init__(self):
        """Initialize instance attributes."""
        self.context = None

    @staticmethod
    @abstractmethod
    def get_common_base():
        """Type of the common base for all classes stored in the same table as this class."""

    @abstractmethod
    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format.

        Notes:

        For composite keys, the embedded keys are concatenated in the
        order of their declaration without brackets.

        Examples:

            - One primary key field A: `A`
            - Two primary key fields A and B: `A;B`
            - Two primary key fields `A1;A2` and `B`: `A1;A2;B`

        Notes:

            Primary key in physical storage or cache may not match this logical primary key format.
            The conversion is performed by the data source implementation.
        """

    def init(self) -> None:
        """Validate dataclass attributes and use them to initialize object state.

        Notes:

            This function will be called by the data source after loading and before saving the object,
            and should also be called every time the object's attributes are updated.

            This implementation in base does nothing. Derived classes can override.
        """

    def __str__(self) -> str:
        """Return primary key by default. Derived classes may override to provide more information.

        Notes:

            Conversion to string is provided for debugging purposes only and may be modified in derived
            classes. Data source implementation must use `get_key` method instead.
        """
        return self.get_key()
