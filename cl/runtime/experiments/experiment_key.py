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
from typing import Type
from cl.runtime.primitive.colon_and_space_delimited_util import ColonAndSpaceDelimitedUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin
from cl.runtime.records.protocols import is_key


@dataclass(slots=True, kw_only=True)
class ExperimentKey(KeyMixin):
    """Run and analyze the results of multiple trials."""

    experiment_id: str = missing()
    """Unique experiment identifier."""

    @classmethod
    def get_key_type(cls) -> Type:
        return ExperimentKey

    def init(self) -> None:
        # Check only if inside a key, will be set automatically if inside a record
        if is_key(self):
            self.check_experiment_id(self.experiment_id)

    @classmethod
    def check_experiment_id(cls, experiment_id: str) -> None:
        """Check that experiment_id does not have semicolon-and-space delimiter."""
        ColonAndSpaceDelimitedUtil.validate(
            value=experiment_id,
            token_count=1,
            value_name="experiment_id",
            data_type="ExperimentKey",
        )
