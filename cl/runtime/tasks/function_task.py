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

import inspect
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.tasks.callable_task import CallableTask
from cl.runtime.tasks.task_key import TaskKey
from dataclasses import dataclass
from typing import Callable
from typing import Type
from typing_extensions import Self


@dataclass(slots=True, kw_only=True)
class FunctionTask(CallableTask):
    """Invoke a function defined in the module directly, do not use for class methods."""

    module: str = missing()
    """Module string in dot-delimited format."""

    function_name: str = missing()
    """Function name in snake_case or PascalCase format."""

    def execute(self) -> None:
        """Invoke the specified static or class method handler."""
        raise NotImplementedError()

    @classmethod
    def from_type(cls, *, task_id: str, record_type: Type, method: Callable, parent: TaskKey | None = None) -> Self:
        """Create from static or class handler method callable."""
        raise NotImplementedError()