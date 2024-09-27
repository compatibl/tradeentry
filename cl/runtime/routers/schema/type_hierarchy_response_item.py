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

from __future__ import annotations
import inspect
from typing import List
from inflection import titleize
from pydantic import BaseModel
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.routers.schema.type_hierarchy_request import TypeHierarchyRequest
from cl.runtime.schema.schema import Schema


class TypeHierarchyResponseItem(BaseModel):
    """Single item of the list returned by the /schema/type-hierarchy route."""

    name: str
    """Class name (may be customized in settings)."""

    label: str
    """Type label displayed in the UI is humanized class name (may be customized in settings)."""

    class Config:
        alias_generator = StringUtil.to_pascal_case
        populate_by_name = True

    @classmethod
    def get_types(cls, request: TypeHierarchyRequest) -> List[TypeHierarchyResponseItem]:
        """Implements /schema/type-hierarchy route."""

        base_type_name = request.name

        # Getting type's successor names
        base_type = Schema.get_type_by_short_name(base_type_name)
        # TODO: Modify the method for removing types to also cover non-abstract Mixins
        successor_types = [t for t in base_type.__subclasses__() if not inspect.isabstract(t)]
        all_type_names = list(set([s_type.__name__ for s_type in successor_types]))
        if not inspect.isabstract(base_type):
            all_type_names.append(base_type_name)

        result = [TypeHierarchyResponseItem(name=type_name, label=titleize(type_name)) for type_name in all_type_names]
        return result
