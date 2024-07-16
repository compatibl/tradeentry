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

from enum import Enum
from typing import Any

from cl.runtime.storage.data_source_types import TDataset

primitive_type_names = ["NoneType", "str", "float", "int", "bool", "date", "time", "datetime", "bytes", "UUID"]
"""Detect primitive type by checking if class name is in this list."""


# TODO: Add checks for custom override of default serializer inside the class
class StringSerializer:
    """Serialize dataset and key to string, flattening hierarchical structure."""

    def serialize_dataset(self, dataset: TDataset) -> Any:
        """Serialize dataset to backslash-delimited string (empty string for None), flattening composite datasets."""

        if dataset is None:
            return ""
        elif dataset.__class__.__name__ in primitive_type_names:
            if isinstance(dataset, str):
                if dataset.startswith("\\") or dataset.endswith("\\"):
                    raise RuntimeError(f"Dataset or dataset token '{dataset}' must not begin or end with backslash.")
                if dataset.startswith(" ") or dataset.endswith(" "):
                    raise RuntimeError(f"Dataset or dataset token '{dataset}' must not begin or end with whitespace.")
            # TODO: Apply rules depending on the specific primitive type
            return str(dataset)
        elif isinstance(dataset, Enum):
            return dataset.name
        elif getattr(dataset, "__iter__", None) is not None:
            return "\\".join(self.serialize_dataset(token) for token in dataset)
        else:
            raise RuntimeError(f"Invalid dataset or its token {dataset}. Valid token types are None, "
                               f"primitive types, enum or their iterables.")

    def serialize_key(self, data):
        """Serialize key to string, flattening for composite keys."""

        key_slots = data.get_key_type().__slots__
        result = ";".join(
            str(v)  # TODO: Apply rules depending on the specific primitive type
            if (v := getattr(data, k)).__class__.__name__ in primitive_type_names
            else v.name
            if isinstance(v, Enum)
            else self.serialize_key(v)
            for k in key_slots
        )
        return result
