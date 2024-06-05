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

import datetime as dt
from stubs.cl.runtime.records.enum.stub_int_enum import StubIntEnum
from typing import Tuple
from typing import Type
from uuid import UUID

StubDataclassPrimitiveFieldsKey = Tuple[
    Type["StubDataclassPrimitiveFields"],
    str,
    float,
    bool,
    int,
    int,  # Long
    dt.date,
    dt.time,
    dt.datetime,
    UUID,
    bytes,
    StubIntEnum,
    # TODO: Add Tuple when added to the class
]
