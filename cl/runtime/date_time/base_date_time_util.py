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

from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseDateTimeUtil(ABC):  # TODO: Refactor to make the API similar to other utilities
    """Interface for date time utils."""

    @staticmethod
    @abstractmethod
    def validate(value: Any) -> None:
        """Validate Date."""
        pass

    @staticmethod
    @abstractmethod
    def to_iso_int(value: Any) -> int:
        """Convert value to iso int."""
        pass

    @staticmethod
    @abstractmethod
    def from_iso_int(iso_int: int) -> Any:
        """Convert iso_int to value."""
        pass

    @staticmethod
    @abstractmethod
    def to_str(value: Any) -> str:
        """Convert value to string interpretation."""
        pass

    @staticmethod
    @abstractmethod
    def from_str(value_str: str) -> Any:
        """Convert string to value."""
        pass
