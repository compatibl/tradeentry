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

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Iterable, List, ClassVar

import inflection


@dataclass(slots=True, frozen=True, init=False)
class RegressionGuard:
    """
    Detects changes (regression) of output across multiple channels during unit testing.

    Notes:
        - The output is recorded in a file named 'channel.received.ext' in the same
          directory as the unit test in which the data was captured
        - If 'channel.expected.ext' does not exist, it is created with the same data
          as 'channel.received.ext'
        - Otherwise 'channel.received.ext' and 'channel.expected.ext' are compared and
          an exception is raised if they differ
        - To record a new 'channel.expected.ext' file, delete the existing one
        - The file extension 'ext' is determined automatically based on which verify methods
          are called
    """

    __stack: ClassVar[List[RegressionGuard]] = []  # TODO: Set using ContextVars
    """New current guard is pushed to the stack using 'with RegressionGuard(...)' clause."""

    base_path: str
    """
    If channel is not specified, the output file path will be 'base_path.received.ext'.
    
    Notes:
        - For tests without a class, base path is 'path_to_test_module.test_method' 
        - For tests inside a class, base path is 'path_to_test_module.test_class.test_method'
          where test_class is the test class name converted to snake case
    """

    channel: str
    """Prefix to the output file names 'channel.received.ext' and 'channel.expected.ext'."""

    def __init__(self, subchannel: str | Iterable[str] | None = None):
        """
        Initialize the guard, optionally specifying dot-delimited subchannel name or its dot-delimited tokens.

        Args:
            subchannel: If specified, dot-delimited subchannel name or its dot-delimited tokens
                        are added to the channel of the current regression guard previously set
                        using 'with RegressionGuard(...)' clause.

                        If the current regression guard is not set, the subchannel is defined relative
                        to the default channel with channel name in 'test_module.test_method' or
                        'test_module.TestClass.test_method' format.
        """

    def verify_text(channel: str, value: Any) -> None:
        """
        Record the value to the specified channel for regression testing purposes.

        Notes:
            - Test output is recorded into a file named 'test_name.method_name.channel.received.txt'
            - Expected test output is recorded into a file named 'test_name.method_name.channel.expected.txt'
            - If the expected test output file for the channel does not exist, it is created
            - Otherwise the received and expected files are compared and the test is considered failed if they differ
        """

    def __enter__(self):
        """Supports `with` operator for resource disposal."""

        # Set current guard on entering 'with RegressionGuard(...)' clause
        self.__stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Supports `with` operator for resource disposal."""

        # Restore the previous current guard on exiting from 'with RegressionGuard(...)' clause
        if len(self.__stack) > 0:
            current_guard = self.__stack.pop()
        else:
            raise RuntimeError("Current regression guard has been modified inside 'with RegressionGuard(...)' clause.")

        if current_guard is not self:
            raise RuntimeError("Current regression guard must only be modified by 'with RegressionGuard(...)' clause.")

        # TODO: Flush channels before closing them

        # Return False to propagate exception to the caller
        return False

    @classmethod
    def current(cls):
        """Return the current regression guard, error message if not set."""
        if len(cls.__stack) > 0:
            return cls.__stack[-1]
        else:
            raise RuntimeError("Current regression guard has not been set, use 'with RegressionGuard(...)' to set.")

    @classmethod
    def get_base_path(cls) -> str:
        """
        Get base path for regression test output by inspecting the stack frame to find the test function or method.

        Notes:
        - For tests without a class, base path is 'path_to_test_module.test_method'
        - For tests inside a class, base path is 'path_to_test_module.test_class.test_method'
          where test_class is the test class name converted to snake case
        """
        stack = inspect.stack()
        for frame_info in stack:
            if frame_info.function.startswith('test_'):
                frame_globals = frame_info.frame.f_globals
                # TODO: module_name = frame_globals['__name__']
                module_file = frame_globals['__file__']
                test_name = frame_info.function
                cls_instance = frame_info.frame.f_locals.get('self', None)
                class_name = cls_instance.__class__.__name__ if cls_instance else None

                if module_file.endswith(".py"):
                    module_path = module_file.removesuffix(".py")
                else:
                    raise RuntimeError(f"Test module file {module_file} does not end with '.py'.")

                if class_name is None:
                    result = f"{module_path}.{test_name}"
                else:
                    class_name = inflection.underscore(class_name)
                    result = f"{module_path}.{class_name}.{test_name}"
                return result

        # If the end of the frame is reached and no function or method starting from test_ is found,
        # the function was not called from inside a test or a custom match pattern is required
        raise RuntimeError("Regression guard must be created inside a function or method that starts from 'test_'.")