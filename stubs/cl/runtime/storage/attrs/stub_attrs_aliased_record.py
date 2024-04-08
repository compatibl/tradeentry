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

from cl.runtime import RecordMixin
from cl.runtime import data_class
from cl.runtime import data_field
from cl.runtime.serialization.type_settings import TypeSettings
from dataclasses import dataclass
from stubs.cl.runtime import StubAttrsRecordKey


@data_class
class StubAttrsAliasedRecord:
    """Stub record class with typename alias."""

    a: int = data_field()


StubAttrsAliasedRecord()

TypeSettings.set_type_alias(StubAttrsAliasedRecord, "StubAttrsAliasedRecordNewName")
