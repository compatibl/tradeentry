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
from cl.runtime.tasks.task import Task
from cl.runtime.testing.regression_guard import RegressionGuard


@dataclass(slots=True, kw_only=True)
class StubTask(Task):
    """Reports its task_id to RegressionGuard during execution."""

    def execute(self) -> None:
        """Reports its task_id to RegressionGuard during execution."""
        RegressionGuard().write(f"Executing StubTask: {self.task_id}")
