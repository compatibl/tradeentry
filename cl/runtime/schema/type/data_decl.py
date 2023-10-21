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
from typing import List, Union

from cl.runtime.schema.type.field_decl import FieldDecl
from cl.runtime.schema.type.type_decl import TypeDecl
from cl.runtime.schema.type.type_decl_key import TypeDeclKey
from cl.runtime.storage.class_field import class_field


@dataclass
class DataDecl(TypeDecl):
    """Declaration for serializable data with fields."""

    parent: Union[str, TypeDeclKey] = class_field(optional=True)
    """Parent type key or record must resolve to DataDecl or its descendants."""

    fields: List[FieldDecl] = class_field()
    """
    List of fields with detailed type information.

    Serialization and front end uses the order of fields inside declaration,
    ordered between classes from base to derived.
    """
