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

from __future__ import annotations

from cl.runtime.schema.type_decl_key import TypeDeclKey
from memoization import cached
from typing import Dict
from typing import Type
from typing_extensions import Self


class Schema:
    """
    Provide declarations for the specified type and all dependencies.
    """

    @classmethod
    def for_key(cls, key: TypeDeclKey) -> Self:
        """Create or return cached object for the specified type declaration key."""
        class_path = f"{key[1][1]}.{key[2]}"  # TODO: Use parse_key method
        return cls.for_class_path(class_path)

    @classmethod
    def for_class_path(cls, class_path: str) -> Self:
        """Create or return cached object for the specified class path in module.ClassName format."""
        raise NotImplementedError()

    @classmethod
    @cached(custom_key_maker=lambda cls, record_type: f"{record_type.__module__}.{record_type.__name__}")
    def for_type(cls, record_type: Type) -> Dict[str, Dict]:
        """
        Declarations for the specified type and all dependencies, returned as a dictionary.

        Args:
            record_type: Type of the record for which the schema is created.
        """
        raise NotImplementedError()
