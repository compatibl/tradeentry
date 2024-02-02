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
from cl.runtime.storage.attrs import attrs_field, attrs_class
from typing import List, Optional

from cl.runtime import Record
from cl.runtime.schema.decl.module_key import ModuleKey
from cl.runtime.schema.decl.package_key import PackageKey


@attrs_class
class Module(ModuleKey, Record):
    """
    Represents a group of related types under a common namespace or directory.
    """

    label: Optional[str] = attrs_field()
    """Module label."""

    comment: Optional[str] = attrs_field()
    """Module additional information."""

    dependences: Optional[List[ModuleKey]] = attrs_field()
    """Module dependences."""

    package: PackageKey = attrs_field()
    """Package refence."""

    copyright_: Optional[str] = attrs_field(name='Copyright')
    """Company name used in Copyright src header."""
