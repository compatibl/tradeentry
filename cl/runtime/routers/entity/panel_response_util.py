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
import base64
import dataclasses
import io
from typing import Any
from typing import Dict
from typing import List
from pydantic import BaseModel
from cl.runtime.context.context import Context
from cl.runtime.plots.plot_key import PlotKey
from cl.runtime.routers.entity.panel_request import PanelRequest
from cl.runtime.routers.response_util import to_legacy_dict
from cl.runtime.routers.response_util import to_record_dict
from cl.runtime.schema.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.schema.schema import Schema
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.views.key_view import KeyView
from cl.runtime.views.pdf_view import PdfView
from cl.runtime.views.plot_view import PlotView
from cl.runtime.views.png_view import PngView

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
            and (found_viewers := [h.name for h in handlers if h.label == request.panel_id and h.type_ == "Viewer"])
        ):
            viewer_name: str = found_viewers[0]
        else:
            raise Exception(f"Type {request.type} has no view with the name {request.panel_id}.")

        # Deserialize key from string to object
        serializer = StringSerializer()
        key_obj = serializer.deserialize_key(data=request.key, type_=type_)

        # Get database from the current context
        db = Context.current().db

        # Load record from the database
        record = db.load_one(type_, key_obj, dataset=request.dataset)
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
    def _get_view_dict(cls, view: Any) -> Dict[str, Any] | None:
        """Convert value to dict format."""

        # Return None if view is None
        if view is None:
            return None

        if isinstance(view, PlotView):
            # Load plot for view if it is key
            plot = Context.current().load_one(PlotKey, view.plot)
            if plot is None:
                raise RuntimeError(f"Not found plot for key {view.plot}.")

            # Get view for plot and transform to ui format dict
            return cls._get_view_dict(plot.get_view())

        elif isinstance(view, KeyView):
            # Load record for view
            record = Context.current().load_one(type(view.key), view.key)
            if record is None:
                raise RuntimeError(f"Not found record for key {view.key}.")

            # Return ui format dict dict of record
            return cls._get_view_dict(record)

        elif isinstance(view, PngView):
            # Return ui format dict of binary data
            return {
                "Content": base64.b64encode(view.png_bytes).decode(),
                "ContentType": "Png",
                "_t": "BinaryContent",
            }
        elif isinstance(view, PdfView):
            # Return ui format dict of binary data
            return {
                "Content": base64.b64encode(view.pdf_bytes).decode(),
                "ContentType": "Pdf",
                "_t": "BinaryContent",
            }
        elif isinstance(view, Dict):
            # Return if is already dict
            return view
        else:
            # TODO (Ina): Do not use a method from dataclasses
            result_type = type(view)
            if result_type.__name__.endswith("Key"):
                view_dict = to_legacy_dict(dataclasses.asdict(view))
                view_dict["_t"] = result_type.__name__
                return view_dict
            else:
                return to_legacy_dict(to_record_dict(view))
