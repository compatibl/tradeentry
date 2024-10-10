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

import ast
import inspect
import textwrap
from typing import List
from typing import Type


class RecordUtil:
    """Utilities for working with records."""

    @classmethod
    def init_all(cls, obj) -> None:
        """Invoke 'init' for each class in class hierarchy that implements it, in the order from base to derived."""

        # Keep track of which init methods in class hierarchy were already called
        invoked = set()

        # Reverse the MRO to start from base to derived
        for class_ in reversed(obj.__class__.__mro__):
            class_init = getattr(class_, "init", None)
            if class_init is not None and (qualname := class_init.__qualname__) not in invoked:
                # Add qualname to invoked to prevent executing the same method twice
                invoked.add(qualname)
                # Invoke 'init' method of superclass if it exists, otherwise do nothing
                class_init(obj)
