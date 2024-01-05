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

from cl.runtime.decorators.data_class_decorator import data_class

from cl.runtime.decorators.data_field_decorator import data_field
from cl.runtime.storage.record import Record


@data_class
class PackageKey(Record):
    """Package is a list of modules and binaries which are deployed together."""

    package_name: str = data_field()
    """Unique package identifier."""

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return self.package_name
