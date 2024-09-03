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
import re
from cl.runtime.context.context import Context
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.schema.schema import Schema
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_key import TaskKey
from dataclasses import dataclass
from inflection import underscore
from typing import Any
from typing import Callable
from typing import Dict
from typing import cast
from typing_extensions import Self

key_serializer = StringSerializer()
param_dict_serializer = DictSerializer()  # TODO: Support complex params


@dataclass(slots=True, kw_only=True)
class InstanceHandlerTask(Task):
    """Executes instance handler of the specified record."""

    record_short_name: str = missing()
    """Record short name as string."""

    key_str: str = missing()
    """Key serialized as semicolon-delimited string."""

    method_name: str = missing()
    """Handler method name."""

    param_dict: Dict = missing()
    """Dictionary of method parameters (None if the method does not have parameters other than self)."""

    def execute(self) -> Any:
        """Invoke the specified instance method handler."""

        # Save self to ensure the worker process loads the same record
        # TODO: Consider creating TaskRun directly with Task object field instead of key
        Context.current().data_source.save_one(self)

        record_type = Schema.get_type_by_short_name(self.record_short_name)
        key_type = record_type().get_key_type()  # TODO: Avoid creating the object to get key type, make classmethod?
        key = key_serializer.deserialize_key(self.key_str, key_type)

        # Load record from storage
        record = Context.current().data_source.load_one(key)
        method_name = self.normalize_method_name(self.method_name)
        method = getattr(record, method_name)  # TODO: Check it is an instance method

        # Pass record as first argument (self) for an instance method
        if self.param_dict is not None:
            method(**self.param_dict)
        else:
            method()

    @classmethod
    def from_key(cls, *, task_id: str, key: KeyProtocol, method: Callable, parent: TaskKey | None = None) -> Self:
        """Create from key and method callable."""

        # Populate known fields
        key_str = key_serializer.serialize_key(key)
        result = cls(task_id=task_id, key_str=key_str, parent=parent)

        # Get method name from callable
        method_tokens = method.__qualname__.split(".")
        if len(method_tokens) == 2:
            # Two tokens means the callable is bound to a class
            result.method_name = method_tokens[1]

            if hasattr(method, "__self__"):
                raise RuntimeError(
                    f"When key is provided separately, method {method.__qualname__} "
                    f"must be specified as 'ClassName.method' rather than 'obj.method'."
                )

        return result

    @classmethod
    def from_instance(cls, *, task_id: str, method: Callable, parent: TaskKey | None = None) -> Self:
        """Create from instance method (record.method_name)."""

        # Populate known fields
        result = cls(task_id=task_id, parent=parent)

        # Get method name from callable
        method_tokens = method.__qualname__.split(".")
        if len(method_tokens) == 2:
            # Two tokens means the callable is bound to a class
            result.method_name = method_tokens[1]

            if hasattr(method, "__self__"):
                if not inspect.isclass(method.__self__):
                    # Assign record instead of key
                    result.key_str = method.__self__.get_key()
                else:
                    raise RuntimeError(
                        f"Method {method.__qualname__} is a class method, " f"use StaticHandlerTask instead."
                    )
            else:
                raise RuntimeError(
                    f"Method {method.__qualname__} is a static method, " f"use StaticHandlerTask instead."
                )
        else:
            raise RuntimeError(
                f"Method {method.__qualname__} is a function rather than a class method, " f"use FunctionTask instead."
            )

        return result

    @classmethod
    def normalize_method_name(cls, method_name: str) -> str:
        """If method name has uppercase letters, assume it is PascalCase and convert to snake_case."""

        if any(c.isupper() for c in method_name):
            # Use inflection library
            result = underscore(method_name)
            # In addition, add underscore before numbers
            result = re.sub(r"([0-9]+)", r"_\1", result)
        else:
            # Already in snake_case, return unchanged argument
            result = method_name
        return result
