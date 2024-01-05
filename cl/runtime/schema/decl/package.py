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

from cl.runtime.decorators.attrs_record_decorator import attrs_record
from typing import List, Optional

from cl.runtime.schema.decl.package_dependency import PackageDependency
from cl.runtime.schema.decl.package_key import PackageKey
from cl.runtime.decorators.data_field_decorator import data_field


@attrs_record
class Package(PackageKey):
    """Package is a list of modules and binaries which are deployed together."""

    package_shortcut: Optional[str] = data_field()
    """
    Unique package shortcut used as a prefix for the type name to resolve possible conflicts in multi-package
    environments.
    """

    comment: Optional[str] = data_field()
    """Comment."""

    label: str = data_field()
    """Label (displayed in user interface, may not be unique)."""

    package_path: Optional[str] = data_field()
    """Relative package path."""

    dependency_search_paths: Optional[List[str]] = data_field()
    """Locations to search dependent packages."""

    dependencies: Optional[List[PackageDependency]] = data_field()
    """Dependent packages list"""

    shared: Optional[bool] = data_field()
    """Package version"""

    version: Optional[str] = data_field()
    """Package version"""

    is_main: Optional[bool] = data_field()
    """Is main package"""
