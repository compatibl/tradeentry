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

from typing import Tuple, Dict
from typing import Type
from cl.runtime.storage.data_source_types import TKey, TPrimitive


class KeyUtil:
    """Utilities for working with keys."""

    @classmethod
    def to_dict(cls, key: TKey) -> Dict[str, TKey | TPrimitive]:
        """Convert key to dictionary using key_fields from its table type."""

        # Get key fields from the table type
        key_fields = key[0].key_fields  # noqa

        # Convert to dictionary, recursively calling to_dict on key elements of a composite key
        return {k: cls.to_dict(v) if isinstance(v, tuple) else v for k, v in zip(key_fields, key[1:])}


    @staticmethod
    def parse_key(key_type: Type, key: Tuple) -> Tuple:
        """Parse key of 'key_type' into a tuple, validating types and flattening composite key contents."""

        # TODO: Support composite types
        record_type = key[0]  # TODO: Check against key type
        result = key[1:]
        return result
