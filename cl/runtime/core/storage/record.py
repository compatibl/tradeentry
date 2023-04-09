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
from cl.runtime.core.storage.data import Data


class Record(Data, ABC):
    """Abstract base class of database records that can be stored in a data source and their keys.

    Final record classes stored in a data source must implement the following methods. Some of these methods may be
    implemented by mixins or intermediate base classes, including those using dataclass and similar frameworks.

    * get_pk(self) - instance method returning primary key without type as semicolon-delimited string,
      for example `A;B` for a class with two primary key fields that have values `A` and `B`
    * to_dict(self) - instance method serializing self as dictionary
    * from_dict(self, data_dict) - instance method populating self from dictionary
    * get_common_base() - static method returning the type of the common base class for all classes
      stored in the same database table as this class.
    """

    context: Optional[Context]
    """
    Context provides platform-independent APIs for:

    * Databases and distributed cache
    * Logging and error reporting
    * Local or remote handler execution
    * Progress reporting
    * Virtualized filesystem
    """

    def __init__(self):
        """Initialize instance attributes."""
        self.context = None

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

    def update(self) -> None:
        """
        Validate properties and set private variables. Invoked by data source before saving and after loading.

        Implementation in base does nothing by default. Derived classes can override.
        """

    def __str__(self) -> str:
        """Return primary key by default. Derived classes may override to provide more information.

        Notes:

            Conversion to string is provided for debugging purposes only and may be modified in derived
            classes. Data source implementation must use `get_pk` method instead.
        """
        return self.get_pk()
