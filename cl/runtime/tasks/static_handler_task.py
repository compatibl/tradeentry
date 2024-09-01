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
from typing import Callable, Dict, Type
from typing_extensions import Self
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.schema.schema import Schema
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_key import TaskKey


@dataclass(slots=True, kw_only=True)
class StaticHandlerTask(Task):
    """Executes static handler of the specified record type."""

    type_name: str = missing()
    """Record type name with optional package alias prefix."""

    method_name: str = missing()
    """Method name."""

    method_type: str = missing()  # TODO: Switch to literal or enum, values are staticmethod or classmethod
    """Static or class method."""

    # TODO: Enable param_dict: Dict = missing()
    """Dictionary of method parameters (None if the method does not have parameters other than cls for classmethod)."""

    def execute(self) -> None:
        """Invoke the specified static or class method handler."""
        record_type = Schema.get_type_by_short_name(self.type_name)
        method = getattr(record_type, self.method_name)

        if self.method_type == "staticmethod":
            if False:  # TODO: Tnable self.param_dict is not None:
                method(**self.param_dict)
            else:
                method()
        elif self.method_type == "classmethod":
            # Pass class as first argument for @classmethod
            if False:  # TODO: Enable parqms, check for self.param_dict is not None:
                method.__func__(record_type, **self.param_dict)
            else:
                method.__func__(record_type)
        else:
            raise RuntimeError(f"Method type {self.method_type} is not 'staticmethod' or 'classmethod'.")

    @classmethod
    def from_type(
        cls,
        *,
        task_id: str,
        record_type: Type,
        method: Callable,
        parent: TaskKey | None = None
    ) -> Self:
        """Create from static or class handler method callable."""

        # Populate known fields
        result = cls(task_id=task_id, type_name=record_type.__name__, parent=parent)

        method_tokens = method.__qualname__.split('.')
        if len(method_tokens) == 2:
            # Two tokens means the callable is bound to a class as expected for a static or class method
            if result.type_name != method_tokens[0]:
                raise RuntimeError(f"Record type specified as input {result.type_name} does not match "
                                   f"the class {method_tokens[0]} of the method callable.")

            # Assign method name
            result.method_name = method_tokens[1]

            # Assign method type (staticmethod or classmethod)
            if hasattr(method, '__self__'):
                # If __self__ is present, check if this is a class indicating a classmethod
                if inspect.isclass(method.__self__):
                    # If method_callable.__self__ is defined and is a class, it is a classmethod
                    result.method_type = "classmethod"
                else:
                    raise RuntimeError(f"Method {method.__qualname__} is not a static or class method.")
            else:
                # Otherwise it is a staticmethod
                result.method_type = "staticmethod"

        return result
