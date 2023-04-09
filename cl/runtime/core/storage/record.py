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
from cl.runtime.core.storage.key import Key


class Record(Data, ABC):
    """
    Base class for database records that can be stored in a document DB,
    relational DB, key-value store, or filesystem.

    Derived classes must implement the following methods:

    * to_pk() - return type and primary key as semicolon-delimited string
    * to_dict() - serialize self as dictionary
    * from_dict(data_dict) - populate self from dictionary
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

    def update(self) -> None:
        """
        Validate properties and set private variables. Invoked by data source before saving and after loading.

        Implementation in base does nothing by default. Derived classes can override.
        """

    @abstractmethod
    def get_type_name(self) -> str:
        """Return unique type name as plain or dot-delimited string according to the user-specified convention.

        The recommended convention is `unique_namespace_alias.ClassName`, or simply `ClassName` if class
        names across all imported modules are unique.

        Examples:

            - `rt.DataSource` and `rt.stubs.StubRecord`
            - `cl.runtime.DataSource` and `cl.runtime.stubs.StubRecord`
            - `DataSource` and `StubRecord` (if class names are unique across all imported modules)

        Notes:

            Type name in physical storage or cache may not match this logical type name format.
            The conversion is performed by the data source implementation.
        """

