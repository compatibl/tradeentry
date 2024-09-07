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

from cl.runtime import ClassInfo
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.schema.schema import Schema
from cl.runtime.tasks.callable_task import CallableTask
from cl.runtime.tasks.task_key import TaskKey
from dataclasses import dataclass
from typing import Callable
from typing import Type
from typing_extensions import Self


@dataclass(slots=True, kw_only=True)
class ClassMethodTask(CallableTask):
    """Invoke a @classmethod, do not use for @staticmethod or instance method."""

    type_str: str = missing()
    """Class type as dot-delimited string in module.ClassName format."""

    method_name: str = missing()
    """The name of @classmethod in snake_case or PascalCase format."""

    def execute(self) -> None:
        """Invoke the specified @classmethod."""

        # Get record type from fully qualified name in module.ClassName format
        record_type = ClassInfo.get_class_type(self.type_str)

        # Method callable is already bound to cls, it is not necessary to pass cls as an explicit parameter
        method = getattr(record_type, self.method_name)

        # Invoke the callable
        method()

    @classmethod
    def create(
            cls,
            *,
            task_id: str,
            parent: TaskKey | None = None,
            record_type: Type,
            method_callable: Callable
    ) -> Self:
        """Create from @classmethod callable and record type."""

        # Populate known fields
        result = cls(task_id=task_id, parent=parent)
        result.type_str = f"{record_type.__module__}.{record_type.__name__}"

        # Check that __self__ is present, otherwise it is a @staticmethod
        if (callable_cls := getattr(method_callable, "__self__", None)) is None or not inspect.isclass(callable_cls):
            raise RuntimeError(f"Callable '{method_callable.__qualname__}' for task_id='{result.task_id}' does not "
                               f"have '__self__' attribute indicating it is a @staticmethod rather than @classmethod, "
                               f"use 'StaticMethodTask' instead of 'ClassMethodTask'.")

        # Two tokens because the callable is bound to a class
        method_tokens = method_callable.__qualname__.split(".")
        if len(method_tokens) == 2:
            # Second token is method name
            result.method_name = method_tokens[1]
        else:
            raise RuntimeError(f"Callable '{method_callable.__qualname__}' for task_id='{result.task_id}' does not "
                               f"have two dot-delimited tokens indicating it is not a method bound to a class.")
        return result
