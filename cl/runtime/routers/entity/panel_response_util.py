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

import ast
import dataclasses
from cl.runtime.context.context import Context
from cl.runtime.routers.entity.panel_request import PanelRequest
from cl.runtime.routers.response_util import to_legacy_dict
from cl.runtime.routers.response_util import to_record_dict
from cl.runtime.schema.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.schema.schema import Schema
from cl.runtime.serialization.string_serializer import StringSerializer
from pydantic import BaseModel
from typing import Any
from typing import Dict
from typing import List

PanelResponseData = Dict[str, Any] | List[Dict[str, Any]] | None


class PanelResponseUtil(BaseModel):
    """Response util for the /entity/panel route."""

    view_of: PanelResponseData
    """Response data type for the /entity/panel route."""

    @classmethod
    def get_content(cls, request: PanelRequest) -> Dict[str, PanelResponseData]:
        """Implements /entity/panel route."""

        # Get type of the record
        type_ = Schema.get_type_by_short_name(request.type)

        # Check if the selected type has the needed viewer and get its name (only viewer's label is provided)
        handlers = HandlerDeclareBlockDecl.get_type_methods(type_).handlers
        if (
            handlers is not None
            and handlers
            and (found_viewers := [h.name for h in handlers if h.label == request.panel_id and h.type_ == "viewer"])
        ):
            viewer_name: str = found_viewers[0]
        else:
            raise Exception(f"Type {request.type} has no view with the name {request.panel_id}.")

        # Deserialize key from string to object
        serializer = StringSerializer()
        key_obj = serializer.deserialize_key(data=request.key, type_=type_)

        # Get data source from the current context
        data_source = Context.current().data_source

        # Load record from the data source
        record = data_source.load_one(type_, key_obj, dataset=request.dataset)
        if record is None:
            raise RuntimeError(
                f"Record with type {request.type} and key {request.key} is not found in dataset {request.dataset}."
            )

        # Call the viewer and get the result
        viewer = getattr(record, viewer_name)
        result_view = viewer()

        # Apply legacy dict conventions
        # TODO (Ina): Optimize speed using dacite or similar library
        if isinstance(result_view, list):
            view_dict = [PanelResponseUtil._get_view_dict(item) for item in result_view]
        else:
            view_dict = PanelResponseUtil._get_view_dict(result_view)

        return {"ViewOf": view_dict}

    @classmethod
    def _get_view_dict(cls, view: Any) -> Dict[str, Any]:
        """Convert value to dict format."""

        if isinstance(view, str):
            view_dict = ast.literal_eval(view)
        elif view is not None:
            # TODO (Ina): Do not use a method from dataclasses
            result_type = type(view)
            if result_type.__name__.endswith("Key"):
                view_dict = to_legacy_dict(dataclasses.asdict(view))
                view_dict["_t"] = result_type.__name__
            else:
                view_dict = to_legacy_dict(to_record_dict(view))
        else:
            view_dict = None
        return view_dict
