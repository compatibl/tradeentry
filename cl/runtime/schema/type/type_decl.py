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

from cl.runtime.storage.record import Record
from cl.runtime.storage.attrs import data_field, data_class
from cl.runtime.schema.type.type_decl_key import TypeDeclKey


@data_class
class TypeDecl(TypeDeclKey, Record):
    """Base class of type declaration in schema."""

    label: str = data_field(optional=True)
    """Readable type label in the front end."""
