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
from typing import Any, Callable
from cl.runtime.records.protocols import KeyProtocol
from typing_extensions import Self
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.storage.data_source_types import TDataDict, TKeyDict
from cl.runtime.context.context import Context
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_key import TaskKey

key_string_serializer = StringSerializer()  # TODO: Support composite keys
param_dict_serializer = DictSerializer()  # TODO: Support complex params


@dataclass(slots=True, kw_only=True)
class InstanceHandlerTask(Task):
    """Executes instance handler of the specified record."""

    key: KeyProtocol = missing()
    """Record for which instance handler will be invoked."""

    method_name: str = missing()
    """Handler method name."""

    param_dict: TDataDict | None = None
    """Dictionary of method parameters (None if the method does not have parameters other than self)."""

    def execute(self) -> Any:
        """Invoke the specified instance method handler."""

        # Load record from storage
        record = Context.current().data_source.load_one(self.key)
        method = getattr(record, self.method_name)  # TODO: Check it is an instance method

        # Pass record as first argument (self) for an instance method
        if self.param_dict is not None:
            method(record, **self.param_dict)
        else:
            method(record)

    @classmethod
    def from_key(
            cls,
            *,
            task_id: str,
            key: KeyProtocol,
            method: Callable,
            parent: TaskKey | None = None
    ) -> Self:
        """Create from key and method callable."""

        # Populate known fields
        result = cls(task_id=task_id, key=key, parent=parent)

        # Get method name from callable
        method_tokens = method.__qualname__.split('.')
        if len(method_tokens) == 2:
            # Two tokens means the callable is bound to a class
            result.method_name = method_tokens[1]

            if hasattr(method, '__self__'):
                raise RuntimeError(f"When key is provided separately, method {method.__qualname__} "
                                   f"must be specified as 'ClassName.method' rather than 'obj.method'.")

        return result

    @classmethod
    def from_instance(
            cls,
            *,
            task_id: str,
            method: Callable,
            parent: TaskKey | None = None
    ) -> Self:
        """Create from instance method (record.method_name)."""

        # Populate known fields
        result = cls(task_id=task_id, parent=parent)

        # Get method name from callable
        method_tokens = method.__qualname__.split('.')
        if len(method_tokens) == 2:
            # Two tokens means the callable is bound to a class
            result.method_name = method_tokens[1]

            if hasattr(method, '__self__'):
                if not inspect.isclass(method.__self__):
                    # Assign record instead of key
                    result.key = method.__self__
                else:
                    raise RuntimeError(f"Method {method.__qualname__} is a class method, "
                                       f"use StaticHandlerTask instead.")
            else:
                raise RuntimeError(f"Method {method.__qualname__} is a static method, "
                                       f"use StaticHandlerTask instead.")
        else:
            raise RuntimeError(f"Method {method.__qualname__} is a function rather than a class method, "
                               f"use FunctionTask instead.")

        return result
