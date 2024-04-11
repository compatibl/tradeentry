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

from cl.runtime.storage.dataset_util import DatasetUtil
from typing import TYPE_CHECKING
from typing import Optional

if TYPE_CHECKING:
    from cl.runtime.storage.data_source import DataSource


class Context:
    """
    Context provides:

    * Default data source
    * Default dataset of the default data source
    * Logging
    * Progress reporting
    * Filesystem access (if available)
    """

    __slots__ = (
        "__data_source",
        "__dataset",
    )

    __data_source: Optional["DataSource"]
    __dataset: Optional[str]

    def __init__(self):
        """
        Set instant variables to None here. They will be
        set and then initialized by the respective
        property setter.
        """

        self.__data_source = None
        """Default data source of the context."""

        self.__dataset = None
        """Default dataset of the context."""

    @property
    def data_source(self) -> "DataSource":
        """Return data_source property, error message if not set."""

        if not self.__data_source:
            raise Exception("Data source property is not set in Context.")
        return self.__data_source

    @data_source.setter
    def data_source(self, value: "DataSource") -> None:
        """Set data_source property and pass self to its init method."""
        self.__data_source = value

    @property
    def dataset(self) -> str:
        """Return dataset property, error message if not set."""

        if self.__dataset is None:
            raise Exception("Dataset property is not set in Context.")
        return self.__dataset

    @dataset.setter
    def dataset(self, value: str) -> None:
        """Set dataset property."""

        if self.__dataset is not None:
            raise ValueError("The dataset field in context is immutable, create a new context instead.")

        # Import inside method to avoid cyclic reference
        from cl.runtime.storage.dataset_util import DatasetUtil

        # Perform validation by converting into tokens, discard the result
        DatasetUtil.to_tokens(value)

        self.__dataset = value

    def __enter__(self):
        """Supports with syntax for resource disposal."""

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Supports with syntax for resource disposal."""

        if self.__data_source is not None:
            self.__data_source.__exit__(exc_type, exc_val, exc_tb)

        # Return False to propagate exception to the caller
        return False
