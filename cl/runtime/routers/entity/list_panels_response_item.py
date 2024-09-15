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
from typing import List
from pydantic import BaseModel
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.routers.entity.list_panels_request import ListPanelsRequest
from cl.runtime.schema.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.schema.schema import Schema


class ListPanelsResponseItem(BaseModel):
    """Data type for a single item in the response list for the /entity/list_panels route."""

    name: str | None
    """Name of the panel."""

    class Config:
        alias_generator = StringUtil.to_pascal_case
        populate_by_name = True

    @classmethod
    def list_panels(cls, request: ListPanelsRequest) -> List[ListPanelsResponseItem]:
        """Implements /entity/list_panels route."""

        # TODO: Return saved view names
        type_ = Schema.get_type_by_short_name(request.type)
        handlers_block = HandlerDeclareBlockDecl.get_type_methods(type_).handlers

        if handlers_block is not None and handlers_block:
            return [
                ListPanelsResponseItem(name=handler.label) for handler in handlers_block if handler.type_ == "viewer"
            ]
        return []
