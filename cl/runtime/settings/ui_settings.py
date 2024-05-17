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

from dataclasses import dataclass
from typing import ClassVar, Dict
from cl.runtime.settings.config import dynaconf_settings


@dataclass(slots=True)
class UiSettings:
    """UI settings do not affect the REST API."""

    __default: ClassVar[UiSettings | None] = None
    """Default instance is initialized from Dynaconf settings."""

    package_labels: Dict[str, str] | str | None = None
    """
    Optional humanized package label in 'pattern: label' format for the UI only.
    Use this feature to organize types by package in large projects and to
    resolve conflicts when classes in different modules share the same class name.
    - For modules that do not match the glob pattern, no package name is used
    - This UI setting does not affect the REST API
    - Dictionary or string in JSON format is accepted
    """

    type_labels: Dict[str, str] | str | None = None
    """
    Replace humanized class name by the specified label for the UI only
    - When not specified, the name is humanized according to ClassName -> Class Name
    - This UI setting does not affect the REST API
    - Dictionary or string in JSON format is accepted
    """

    field_labels: Dict[str, str] | str | None = None
    """
    Replace humanized field name by the specified label for the UI only
    - When not specified, the name is humanized according to field_name -> Field Name
    - This UI setting does not affect the REST API
    - Dictionary or string in JSON format is accepted
    """

    method_labels: Dict[str, str] | str | None = None
    """
    Replace humanized method name by the specified label for the UI only
    - When not specified, the name is humanized according to method_name -> Method Name
    - This UI setting does not affect the REST API
    - Dictionary or string in JSON format is accepted
    """

    item_labels: Dict[str, str] | str | None = None
    """
    Replace humanized method name by the specified enum item (member) for the UI only
    - When not specified, the name is humanized according to ITEM_NAME -> Item Name
    - This UI setting does not affect the REST API
    - Dictionary or string in JSON format is accepted
    """

    @staticmethod
    def default() -> UiSettings:
        """Default instance is initialized from Dynaconf settings."""

        if UiSettings.__default is None:
            # Load from Dynaconf settings on first call
            ui_settings_dict = dynaconf_settings["ui_settings"]
            UiSettings.__default = UiSettings(**ui_settings_dict)
        return UiSettings.__default
