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
from typing_extensions import Self
from typing import Any


class DataMixin(ABC):
    """
    Declares abstract methods that provide serialization and deserialization to classes that
    do not have __slots__ or do not store data in fields.

    Notes:
        The use of this class is optional. The code must not rely on inheritance from this class.
    """

    @abstractmethod
    def serialize_data(self, serializer) -> Any:  # TODO: Specify type hint for SerializerProtocol
        """Serialize self, calling the specified serializer for fields that do not implement serialize_data."""
        # TODO: Consider renaming to pack and unpack (for key as well, to avoid name clashes)

    @classmethod
    @abstractmethod
    def deserialize_data(cls, data: Any, serializer) -> Self: # TODO: Specify type hint for SerializerProtocol
        """Deserialize data, calling the specified serializer for fields that do not implement deserialize_data."""
