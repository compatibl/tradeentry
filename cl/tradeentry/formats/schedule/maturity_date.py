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

from dataclasses import dataclass
from cl.runtime.records.record_mixin import RecordMixin
from cl.tradeentry.formats.schedule.maturity_date_key import MaturityDateKey


@dataclass(slots=True, kw_only=True)
class MaturityDate(MaturityDateKey, RecordMixin[MaturityDateKey]):
    """Trade or leg maturity date defined as unadjusted date or time interval relative to another date."""

    def get_key(self) -> MaturityDateKey:
        return MaturityDateKey(maturity_date_id=self.maturity_date_id)
