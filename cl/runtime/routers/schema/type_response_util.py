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
from typing import Dict
from cl.runtime.routers.schema.type_request import TypeRequest


class TypeResponseUtil:
    """Response helper class for the /schema/typeV2 route."""

    @staticmethod
    def get_type(request: TypeRequest) -> Dict[str, int]:
        """Implements /storage/get_datasets route."""

        # TODO: Default response
        result_dict = {
          "name": 1,
        }

        return result_dict


