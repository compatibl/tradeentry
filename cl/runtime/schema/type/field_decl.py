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

from cl.runtime.storage.attrs_data_util import attrs_data
from cl.runtime.storage.attrs import attrs_field, attrs_class
from typing import Union

from cl.runtime.schema.type.type_decl_key import TypeDeclKey
from cl.runtime.storage.data import Data


@attrs_data
class FieldDecl(Data):
    """Base class of type declaration in schema."""

    name: str = attrs_field()
    """Field name in code and storage."""

    label: str = attrs_field(optional=True)
    """Readable field label in the front end."""

    type: Union[str, TypeDeclKey] = attrs_field()
    """Field type."""

    dim: int = attrs_field(optional=True)
    """List, array, or tensor dimension (defaults to scalar, i.e., the value of zero, if not specified)."""

    optional: bool = attrs_field(optional=True)
    """True if field is optional (defaults to required if not specified)."""

    contains_optional: bool = attrs_field(optional=True)
    """True if list, array, or tensor elements are optional (defaults to required if not specified)."""
