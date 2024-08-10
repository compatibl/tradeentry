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

from cl.runtime.settings.settings import Settings
from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True, kw_only=True, frozen=True)
class UiSettings(Settings):
    """UI settings are for visual presentation to the user only. They do not affect the REST API."""

    package_labels: Dict[str, str] | None = None
    """
    Custom package alias labels as a dictionary in 'package_alias: Package Label' format for the UI only.
    
    Notes:
        - Use this feature to provide custom labels for package aliases.
        - It does not apply when package_aliases are not specified in api_settings
        - When custom label is not specified, the package alias is humanized as package_alias -> Package Alias
        - This UI setting does not affect the REST API
    """

    type_labels: Dict[str, str] | None = None
    """
    Custom record type labels as a dictionary in 'ClassName: Class Label' format for the UI only.

    Notes:
        - When not specified, the label is humanized as ClassName -> Class Name
        - This UI setting does not affect the REST API
    """

    field_labels: Dict[str, str] | None = None
    """
    Custom field labels as a dictionary in 'field_name: Field Name' format for the UI only.
    
    Notes:
    - When not specified, the label is humanized as field_name -> Field Name
    - This UI setting does not affect the REST API
    """

    method_labels: Dict[str, str] | None = None
    """
    Custom method labels as a dictionary in 'method_name: Method Name' format for the UI only.
    
    Notes:
    - When not specified, the name is humanized as method_name -> Method Name
    - This UI setting does not affect the REST API
    """

    enum_item_labels: Dict[str, str] | None = None
    """
    Custom enum item labels as a dictionary in 'ITEM_NAME: Item Name' format for the UI only.
    
    Notes:
    - When not specified, the name is humanized as ITEM_NAME -> Item Name
    - This UI setting does not affect the REST API
    """

    @classmethod
    def get_settings_path(cls) -> str:
        return "runtime.ui_settings"
