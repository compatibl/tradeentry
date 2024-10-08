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

from pydantic import BaseModel
from cl.runtime import Context
from cl.runtime.routers.entity.save_request import SaveRequest
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.serialization.ui_dict_serializer import UiDictSerializer

data_serializer = UiDictSerializer()
key_serializer = StringSerializer()


class SaveResponse(BaseModel):
    """Data type for the /entity/save response."""

    key: str | None
    """String representation of the key for the saved record."""

    class Config:
        populate_by_name = True

    @staticmethod
    def save_entity(request: SaveRequest) -> "SaveResponse":
        """Save entity."""
        context = Context.current()

        # Get ui record and apply ui conversion
        ui_record = request.record_dict.model_dump()

        # TODO (Roman): fix on ui
        # Workaround for UiAppState request. Ui send OpenedTabs without _t
        if ui_record.get("_t") == "UiAppState" and (opened_tabs := ui_record.get("OpenedTabs")) is not None:
            # Add _t to each TabInfo in list
            ui_record["OpenedTabs"] = [
                {
                    **{k: v for k, v in item.items() if k != "Type"},
                    "Type": {**item["Type"], "_t": "BaseTypeInfo"},
                    "_t": "TabInfo",
                }
                for item in opened_tabs
            ]

        # TODO (Roman): align UiTypeState data model and UiTypeState dict from ui
        # Skip saving UiTypeState object
        if ui_record.get("_t") == "UiTypeState":
            return SaveResponse(key=None)

        prepared_serialized_record = data_serializer.apply_ui_conversion(ui_record)

        # Deserialize record
        record = data_serializer.deserialize_data(prepared_serialized_record)

        if request.old_record_key is None:
            existing_record = context.load_one(
                record_type=type(record),
                record_or_key=record.get_key(),
                dataset=request.dataset,
            )
            if existing_record is not None:
                raise RuntimeError(f"Record with key {str(record)} already exists.")

        if request.old_record_key is not None and request.old_record_key != key_serializer.serialize_key(record):
            old_record_key_obj = key_serializer.deserialize_key(request.old_record_key, type(record.get_key()))
            context.delete_one(key_type=type(record.get_key()), key=old_record_key_obj, dataset=request.dataset)
        context.save_one(record, dataset=request.dataset)

        return SaveResponse(key=key_serializer.serialize_key(record))
