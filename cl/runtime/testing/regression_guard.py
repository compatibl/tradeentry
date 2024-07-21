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
import inflection
from dataclasses import dataclass
from typing import Any, Iterable, List, ClassVar, cast


@dataclass(slots=True, init=False)
class RegressionGuard:
    """
    Detects changes (regression) of output across multiple channels during unit testing.

    Notes:
        - Channel name is module.test_function or module.test_class.test_method
        - The output is recorded in 'channel.received.ext' located next to the unit test
        - If 'channel.expected.ext' does not exist, it is created with the same data as 'channel.received.ext'
        - Otherwise, the test fails if 'channel.expected.ext' and 'channel.received.ext' differ
        - To record a new 'channel.expected.ext' file, delete the existing one
        - File extension 'ext' is determined based on the verify method(s) called
    """

    __stack: ClassVar[List[RegressionGuard]] = []  # TODO: Set using ContextVars
    """New current guard is pushed to the stack using 'with RegressionGuard(...)' clause."""

    output_path: str
    """Output path including directory and channel."""

    ext: str | None = None
    """Output file extension depends on the verify method(s) called."""

    def __init__(self, *, subchannel: str | Iterable[str] | None = None):
        """
        Initialize the regression guard, optionally specifying subchannel.

        Args:
            subchannel: Dot-delimited string or an iterable of dot-delimited tokens added to the current channel
        """

        # Check if current regression guard is set
        if len(self.__stack) == 0:
            # Current regression guard is not set, find output path by examining call stack
            output_path = self.get_output_path()
        else:
            # Obtain defaults from the current regression guard
            output_path = self.current().output_path

        if subchannel is not None:
            if isinstance(subchannel, str):
                # TODO: Use specialized conversion for primitive types
                subchannel = str(subchannel)
            elif hasattr(subchannel, "__iter__"):
                # TODO: Use specialized conversion for primitive types
                subchannel = ".".join([str(x) for x in subchannel])
            else:
                raise RuntimeError("Output channel must be a primitive type or an iterable of primitive types.")

            if subchannel != "":
                output_path = f"{output_path}.{subchannel}"

        # Set output path
        self.output_path = output_path

    def verify_text(self, channel: str, value: Any) -> None:
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
            raise RuntimeError("Current regression guard is cleared inside 'with RegressionGuard(...)' clause.")

        if current_guard is not self:
            raise RuntimeError("Current regression guard is modified inside 'with RegressionGuard(...)' clause.")

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
    def get_output_path(cls) -> str:
        """
        Return the tuple of absolute directory path and module name of the test
        inside which this method was invoked by searching the stack frame for 'test_' or a custom
        test function name pattern.
        """

        stack = inspect.stack()
        for frame_info in stack:
            if frame_info.function.startswith('test_'):
                frame_globals = frame_info.frame.f_globals
                module_file = frame_globals['__file__']
                test_name = frame_info.function
                cls_instance = frame_info.frame.f_locals.get('self', None)
                class_name = cast(type, cls_instance).__class__.__name__ if cls_instance else None

                if module_file.endswith(".py"):
                    module_file_without_ext = module_file.removesuffix(".py")
                else:
                    raise RuntimeError(f"Test module file {module_file} does not end with '.py'.")

                if class_name is None:
                    result = f"{module_file_without_ext}.{test_name}"
                else:
                    class_name = inflection.underscore(class_name)
                    result = f"{module_file_without_ext}.{class_name}.{test_name}"
                return result

        # If the end of the frame is reached and no function or method starting from test_ is found,
        # the function was not called from inside a test or a custom match pattern is required
        raise RuntimeError("Regression guard must be created inside a function or method that starts from 'test_'.")
