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

from cl.runtime.records.dataclasses.dataclass_mixin import DataclassMixin
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.schema.package_decl_key import PackageDeclKey
from dataclasses import dataclass


@dataclass(slots=True)
class PackageDecl(DataclassMixin):
    """Package is a list of modules and binaries which are deployed together."""

    package_name: str = datafield()
    """Unique package identifier."""

    comment: str | None = datafield()
    """Comment."""

    copyright_: str | None = datafield(name="Copyright")
    """Copyright used for given package."""

    alias: str | None = datafield()
    """Short alias used in submodule naming."""

    label: str | None = datafield()
    """Label (displayed in user interface, may not be unique)."""

    def get_key(self) -> PackageDeclKey:
        return type(self), self.package_name
