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
from cl.runtime.experiments.experiment_key import ExperimentKey
from cl.runtime.experiments.trial_key import TrialKey
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin


@dataclass(slots=True, kw_only=True)
class Trial(TrialKey, RecordMixin[TrialKey]):
    """Run and store the result of a single trial for the specified experiment."""

    experiment: ExperimentKey = missing()
    """Experiment for which the trial is performed."""

    trial_label: str = missing()
    """Identifier of the trial is unique within the experiment."""

    def get_key(self) -> TrialKey:
        return TrialKey(trial_id=self.trial_id)

    def init(self) -> None:
        """Generate trial_id in 'ExperimentId: TrialLabel' format."""
        self.trial_id = self.get_trial_id(self.experiment, self.trial_label)
