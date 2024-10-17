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
from abc import ABC
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import Dict
from typing import cast
from inflection import underscore
from typing_extensions import Self
from cl.runtime.context.context import Context
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.protocols import KeyProtocol
from cl.runtime.schema.schema import Schema
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_key import TaskKey

key_serializer = StringSerializer()
param_dict_serializer = DictSerializer()  # TODO: Support complex params


@dataclass(slots=True, kw_only=True)
class CallableTask(Task, ABC):
    """Base class for tasks that invoke callables (class methods, functions, etc.)."""

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
