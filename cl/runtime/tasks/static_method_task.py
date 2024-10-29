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
from dataclasses import dataclass
from typing import Callable
from typing import Type
from typing_extensions import Self
from cl.runtime import ClassInfo
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.schema.schema import Schema
from cl.runtime.tasks.callable_task import CallableTask
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.tasks.task_queue_key import TaskQueueKey


@dataclass(slots=True, kw_only=True)
class StaticMethodTask(CallableTask):
    """Invoke a @staticmethod or @classmethod, do not use for instance methods."""

    type_str: str = missing()
    """Class type as dot-delimited string in module.ClassName format."""

    method_name: str = missing()
    """The name of @staticmethod in snake_case or PascalCase format."""

    def run_task(self) -> None:
        """Invoke the specified @staticmethod or @classmethod."""

        # Get record type from fully qualified name in module.ClassName format
        record_type = ClassInfo.get_class_type(self.type_str)

        # Method callable is already bound to cls, it is not necessary to pass cls as an explicit parameter
        method_name = self.normalize_method_name(self.method_name)
        method = getattr(record_type, method_name)

        # Invoke the callable
        method()

    @classmethod
    def create(
            cls,
            *,
            queue: TaskQueueKey,
            record_type: Type,
            method_callable: Callable,
    ) -> Self:
        """Create from @staticmethod callable and record type."""

        # Populate known fields
        result = cls(queue=queue)
        result.type_str = f"{record_type.__module__}.{record_type.__name__}"

        # Check that __self__ is either absent (@staticmethod) or is a class (@classmethod)
        if (method_cls := getattr(method_callable, "__self__", None)) is not None and not inspect.isclass(method_cls):
            raise RuntimeError(
                f"Callable '{method_callable.__qualname__}' for task_id='{result.task_id}' is "
                f"an instance method rather than @staticmethod or @classmethod, "
                f"use 'InstanceMethodTask' instead of 'StaticMethodTask'."
            )

        # Two tokens because the callable is bound to a class
        method_tokens = method_callable.__qualname__.split(".")
        if len(method_tokens) == 2:
            # Second token is method name
            result.method_name = method_tokens[1]
        else:
            raise RuntimeError(
                f"Callable '{method_callable.__qualname__}' for task_id='{result.task_id}' does not "
                f"have two dot-delimited tokens indicating it is not a method bound to a class."
            )
        return result
