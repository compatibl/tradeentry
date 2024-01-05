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
from typing import Union

from cl.runtime.schema.type.type_decl_key import TypeDeclKey
from cl.runtime.storage.class_data import ClassData
from cl.runtime.decorators.data_field_decorator import data_field


@data_class
class FieldDecl(ClassData):
    """Base class of type declaration in schema."""

    name: str = data_field()
    """Field name in code and storage."""

    label: str = data_field(optional=True)
    """Readable field label in the front end."""

    type: Union[str, TypeDeclKey] = data_field()
    """Field type."""

    dim: int = data_field(optional=True)
    """List, array, or tensor dimension (defaults to scalar, i.e., the value of zero, if not specified)."""

    optional: bool = data_field(optional=True)
    """True if field is optional (defaults to required if not specified)."""

    contains_optional: bool = data_field(optional=True)
    """True if list, array, or tensor elements are optional (defaults to required if not specified)."""
