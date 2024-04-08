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

from logging import getLogger
from typing import Dict
from typing import Type

logger = getLogger(__name__)  # TODO: Use standard way to get default logger


class TypeSettings:
    """Customize type attributes that would otherwise be obtained from source code."""

    __type_alias_dict: Dict[str, str] = dict()

    @staticmethod
    def get_type_alias(type_: Type | str) -> str:
        """
        Get type alias for use in REST and UI (in case of UI, label will override).
        Returns `type_.__name__` if alias is not set.
        """
        # Argument is either type or full type path
        if isinstance(type_, type):
            type_path = f"{type_.__module__}.{type_.__name__}"
            typename = type_.__name__
        elif isinstance(type_, str):
            type_path = type_
            typename = type_.rsplit(".", 1)[-1]
        else:
            raise TypeError("First argument of `TypeSettings.get_type_alias` must be either path or string.")

        # Return typename if alias is not already set
        result = TypeSettings.__type_alias_dict.setdefault(type_path, typename)
        return result

    @staticmethod
    def set_type_alias(type_: Type | str, type_alias: str) -> None:
        """
        Set type alias for use in REST and UI (in case of UI, label will override).

        - The alias is only for the typename and does not affect module.
        - To prioritize override via settings, the first alias to be set will prevail.
        """
        # Argument is either type or full type path
        type_path = f"{type_.__module__}.{type_.__name__}" if isinstance(type_, type) else type_

        # This will do nothing when value is already set
        type_name = TypeSettings.__type_alias_dict.setdefault(type_path, type_alias)

        # Log an attempt to override already set value
        if type_name != type_alias:
            logger.warning(f"Alias {type_alias} for {type_path} is ignored because alias already exists for this type.")
