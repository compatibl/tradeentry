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

from typing import Any
from typing import Protocol

from cl.runtime.storage.data_source_types import TDataset


class DatasetSerializerProtocol(Protocol):
    """Protocol for dataset serialization, deserialization is not required."""

    def serialize_dataset(self, dataset: TDataset) -> Any:
        """Serialize dataset (result type depends on the serializer)."""


class KeySerializerProtocol(Protocol):
    """Protocol for key serialization, deserialization is not required."""

    def serialize_key(self, key: Any) -> Any:
        """Serialize key (argument and result type depend on the serializer)."""


class DataSerializerProtocol(Protocol):
    """Protocol for data serialization and deserialization."""

    def serialize_data(self, data: Any) -> Any:
        """Serialize object (argument and result type depend on the serializer)."""

    def deserialize_data(self, data: Any) -> Any:
        """Serialize object (argument and result type depend on the serializer)."""
