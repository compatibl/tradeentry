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

from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.schema.type_decl_key import TypeDeclKey
from dataclasses import dataclass


@dataclass
class FieldDecl:
    """Base class of type declaration in schema."""

    name: str = datafield()
    """Field name in code and storage."""

    label: str = datafield(optional=True)
    """Readable field label in the front end."""

    type: TypeDeclKey = datafield()
    """Field type."""

    dim: int = datafield(optional=True)
    """List, array, or tensor dimension (defaults to scalar, i.e., the value of zero, if not specified)."""

    optional: bool = datafield(optional=True)
    """True if field is optional (defaults to required if not specified)."""

    contains_optional: bool = datafield(optional=True)
    """True if list, array, or tensor elements are optional (defaults to required if not specified)."""
