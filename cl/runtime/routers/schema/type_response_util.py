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

from cl.runtime.routers.schema.type_request import TypeRequest
from typing import Dict

from cl.runtime.schema.schema import Schema


class TypeResponseUtil:
    """Response helper class for the /schema/typeV2 route."""

    @staticmethod
    def get_type(request: TypeRequest) -> Dict[str, Dict]:
        """Implements /storage/get_datasets route."""

        # TODO: Check why empty module is passed, is module the short name prefix?
        record_type = Schema.get_type_by_short_name(request.name)
        result = Schema.for_type(record_type)
        return result
