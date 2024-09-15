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
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_mixin import KeyMixin


@dataclass(slots=True, kw_only=True)
class WorkflowPhaseKey(KeyMixin):
    """
    Determines the order of task execution within the workflow.

    Notes:
        - Each task is assigned a single phase
        - Tasks run in parallel within each phase, in the order of phases
        - Running tasks can create new tasks assigned to the same phase or subsequent phases
        - If a list of 'prerequisites' is specified, the workflow will ensure that all prerequisite phases
          are completed before this phase begins
    """

    phase_id: str = missing()
    """Unique workflow phase identifier."""

    @classmethod
    def get_key_type(cls) -> Type:
        return WorkflowPhaseKey
