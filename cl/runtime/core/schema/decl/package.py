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

from dataclasses import dataclass
from typing import List, Optional

from cl.runtime.core.schema.decl.package_dependency import PackageDependency
from cl.runtime.core.schema.decl.package_key import PackageKey
from cl.runtime.core.storage.class_field import class_field


@dataclass
class Package(PackageKey):
    """Package is a list of modules and binaries which are deployed together."""

    package_shortcut: Optional[str] = class_field()
    """
    Unique package shortcut used as a prefix for the type name to resolve possible conflicts in multi-package
    environments.
    """

    comment: Optional[str] = class_field()
    """Comment."""

    label: str = class_field()
    """Label (displayed in user interface, may not be unique)."""

    package_path: Optional[str] = class_field()
    """Relative package path."""

    dependency_search_paths: Optional[List[str]] = class_field()
    """Locations to search dependent packages."""

    dependencies: Optional[List[PackageDependency]] = class_field()
    """Dependent packages list"""

    shared: Optional[bool] = class_field()
    """Package version"""

    version: Optional[str] = class_field()
    """Package version"""

    is_main: Optional[bool] = class_field()
    """Is main package"""
