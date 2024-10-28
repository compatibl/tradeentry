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
from cl.runtime.exceptions.error_message_util import ErrorMessageUtil
from cl.runtime.experiments.experiment_key import ExperimentKey
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.colon_and_space_delimited_util import ColonAndSpaceDelimitedUtil
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin
from cl.runtime.records.protocols import is_key


@dataclass(slots=True, kw_only=True)
class TrialKey(KeyMixin):
    """Run and store the result of a single trial for the specified experiment."""

    trial_id: str = missing()
    """Unique identifier of the trial using 'ExperimentId: TrialLabel' format."""

    @classmethod
    def get_key_type(cls) -> Type:
        return TrialKey

    def init(self) -> None:
        # Check only if inside a key, will be set automatically if inside a record
        if is_key(self):
            self.check_trial_id(self.trial_id)

    @classmethod
    def get_trial_id(cls, experiment: ExperimentKey, trial_label: str) -> str:
        """Generate trial_id in 'ExperimentId: TrialLabel' format."""
        if experiment is None:
            raise ErrorMessageUtil.value_error(
                value=None,
                value_name="experiment",
                data_type="TrialKey",
            )
        if experiment.experiment_id is None:
            raise ErrorMessageUtil.value_error(
                value=None,
                value_name="experiment_id",
                data_type="ExperimentKey",
            )
        if trial_label is None:
            raise ErrorMessageUtil.value_error(
                value=None,
                value_name="trial_label",
                data_type="TrialKey",
            )
        trial_id = f"{experiment.experiment_id}: {trial_label}"
        cls.check_trial_id(trial_id)
        return trial_id

    @classmethod
    def check_trial_id(cls, trial_id: str) -> None:
        """Check that trial_id has the expected 'ExperimentId: TrialLabel' format."""
        ColonAndSpaceDelimitedUtil.validate(
            value=trial_id,
            token_count=2,
            value_name="the argument of",
            method_name="check_trial_id",
            data_type="TrialKey",
        )
