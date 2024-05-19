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
from typing import List, Optional, Tuple, Type
from cl.runtime.schema.package_key import PackageKey
from cl.runtime.records.dataclasses.dataclass_mixin import datafield, DataclassMixin
from cl.runtime.schema.module_key import ModuleKey


class Module(DataclassMixin, ABC):
    """
    Defines Analyst module. Module can be represented both as the source code and precomiled dll (defined by flag
    'Compiled').
    """

    module_name: str | None = datafield()
    """Unique module identifier in dot delimited format."""

    label: str | None = datafield()
    """Module label."""

    comment: str | None = datafield()
    """Module additional information."""

    dependences: Optional[List[ModuleKey]] = datafield()
    """Module dependences."""

    package: PackageKey = datafield()
    """Package reference."""

    copyright_: str | None = datafield(name='Copyright')
    """Company name used in Copyright src header."""

    def get_key(self) -> ModuleKey:
        return type(self), self.module_name
