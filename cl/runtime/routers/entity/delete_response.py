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
from cl.runtime.routers.entity.delete_request import DeleteRequest
from cl.runtime.serialization.dict_serializer import get_type_dict
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.serialization.ui_dict_serializer import UiDictSerializer

data_serializer = UiDictSerializer()
key_serializer = StringSerializer()


class DeleteResponse(BaseModel):
    """Data type for the /entity/delete_many response."""

    @staticmethod
    def delete_many(request: DeleteRequest) -> 'DeleteResponse':
        """Delete entities."""
        context = Context.current()
        type_dict = get_type_dict()

        record_key_dicts = [key.model_dump() for key in request.record_keys]
        deserialized_record_keys = [
            key_serializer.deserialize_key(
                key["_key"],
                type_dict[key["_t"]].get_key_type()
            )
            for key in record_key_dicts
        ]
        context.delete_many(deserialized_record_keys, dataset=request.dataset)

        return DeleteResponse()
