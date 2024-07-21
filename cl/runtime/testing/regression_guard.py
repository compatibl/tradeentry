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

import difflib
import filecmp
import inspect
import os

import inflection
import yaml
from dataclasses import dataclass, field
from typing import Any, Iterable, List, ClassVar, cast, Dict, Set

from cl.runtime.schema.field_decl import primitive_types

supported_extensions = ["txt"]


def error_channel_not_primitive_type() -> Any:
    raise RuntimeError("Output channel must be a primitive type or an iterable of primitive types.")


def error_extension_not_supported(ext: str) -> Any:
    raise RuntimeError(f"Extension {ext} is not supported by RegressionGuard. "
                       f"Supported extensions: {', '.join(supported_extensions)}")


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

    __output_path_set: ClassVar[Set[str]] = set()  # TODO: Set using ContextVars
    """Set of output_path for the existing guards, used to prevent creating two guards with the same output_dir."""

    __stack: ClassVar[List[RegressionGuard]] = []  # TODO: Set using ContextVars
    """New current guard is pushed to the stack using 'with RegressionGuard(...)' clause."""

    output_path: str
    """Output path including directory and channel."""

    ext: str
    """Output file extension, defaults to '.txt'"""

    is_verified: bool
    """Verify method sets this flag to true, after which further writes raise an error."""

    def __init__(self, *, ext: str = None, channel: str | Iterable[str] | None = None):
        """
        Initialize the regression guard, optionally specifying channel.

        Args:
            channel: Dot-delimited string or an iterable of dot-delimited tokens added to the current channel
        """

        # Check if current regression guard is set
        if len(self.__stack) == 0:
            # Current regression guard is not set, set output path by examining call stack
            output_path = self.get_output_path()
        else:
            # Set output path to the same value as the current regression guard
            current_guard = self.current()
            output_path = current_guard.output_path
            # Same for extension but only if not specified as parameter
            if ext is None:
                ext = current_guard.ext

        # Append channel if specified
        output_path = self.get_output_path_with_channel(output_path, channel)

        # Check if regression guard already exists for this output path
        if output_path in self.__output_path_set:
            # Error if already exists
            raise RuntimeError(f"Regression guard already exists for output path {output_path}, use the existing "
                               f"guard directly or using 'with RegressionGuard(...)' clause.")
        else:
            # Add to the set otherwise
            self.__output_path_set.add(output_path)

        if ext is not None:
            # Remove dot prefix if specified
            ext = ext.removeprefix(".")
            if ext not in supported_extensions:
                error_extension_not_supported(ext)
        else:
            # Use txt if not specified and not obtained from the current regression guard
            ext = "txt"

        # Set field values
        self.output_path = output_path
        self.ext = ext
        self.is_verified = False

        # Delete the existing received file if exists
        if os.path.exists(received_file := self.get_received_path()):
            os.remove(received_file)

    def write(self, value: Any) -> None:
        """
        Record the argument for regression testing purposes.

        Args:
            value: Data to be recorded, accepted data types depend on the specified file extension
        """
        if self.is_verified:
            raise RuntimeError(f"Regression output file {self.get_received_path()} is already verified "
                               f"and can no longer be written to.")

        if self.ext == "txt":
            with open(self.get_received_path(), 'a') as file:
                file.write(self.format_txt(value))
                # Flush immediately to ensure all of the output is on disk in the event of test exception
                file.flush()
        else:
            # Should not be reached here because of a previous check in __init__
            error_extension_not_supported(self.ext)

    def verify(self) -> None:
        """
        Verify that 'channel.received.ext' is the same as 'channel.expected.ext', or if 'channel.expected.ext'
        does not exist, copy the data from 'channel.received.ext'.
        """

        if self.is_verified:
            # Already verified, exit
            return
        else:
            # Otherwise set 'verified' flag
            self.is_verified = True

        received_path = self.get_received_path()
        expected_path = self.get_expected_path()

        if os.path.exists(expected_path):
            # Expected file exists, compare
            if not filecmp.cmp(received_path, expected_path, shallow=False):
                # Raise an error with unified diff
                with open(received_path, 'r') as received_file, open(expected_path, 'r') as expected_file:
                    received_lines = received_file.readlines()
                    expected_lines = expected_file.readlines()
                    diff = difflib.unified_diff(
                        expected_lines,
                        received_lines,
                        fromfile=expected_path,
                        tofile=received_path
                    )
                    # Limit diff to 5 lines
                    diff = list(diff)
                    if len(diff) > 5:
                        regression_error = "Regression test diff (truncated to 5 lines):\n" + "\n".join(diff[:5]) + "\n"
                    else:
                        regression_error = "Regression test diff:\n" + "\n".join(diff) + "\n"
                    raise RuntimeError(regression_error)
        else:
            # Copy the data from received to expected
            with open(received_path, 'rb') as received_file, open(expected_path, 'wb') as expected_file:
                expected_file.write(received_file.read())

    def __enter__(self):
        """Supports `with` operator for resource disposal."""

        # Set current guard on entering 'with RegressionGuard(...)' clause
        self.__stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Supports `with` operator for resource disposal."""

        # Verify self
        self.verify()

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
        
    def format_txt(self, value: Any) -> str:
        """Format text for regression testing."""
        value_type = type(value)
        if value_type in primitive_types:
            # TODO: Use specialized conversion for primitive types
            return str(value) + "\n"
        elif value_type == dict:
            return yaml.dump(value, default_flow_style=False) + "\n"
        elif hasattr(value_type, "__iter__"):
            return "\n".join(map(self.format_txt, value)) + "\n"
        else:
            raise RuntimeError(f"Argument type {value_type} is not accepted for file extension '{self.ext}'. "
                               f"Valid arguments are primitive types, dict, or their iterable.")

    def get_received_path(self) -> str:
        """The output is recorded in 'channel.received.ext' located next to the unit test."""
        return f"{self.output_path}.received.{self.ext}"

    def get_expected_path(self) -> str:
        """The output is compared to 'channel.expected.ext' located next to the unit test."""
        return f"{self.output_path}.expected.{self.ext}"

    @classmethod
    def get_output_path_with_channel(cls, output_path: str, channel: str | Iterable[str] | None) -> str:
        """The output is recorded in 'channel.received.ext' located next to the unit test."""

        if channel is not None:
            if isinstance(channel, primitive_types):  # TODO: Move primitive_types to another module
                # TODO: Use specialized conversion for primitive types
                channel = str(channel)
            elif hasattr(channel, "__iter__"):
                # TODO: Use specialized conversion for primitive types
                channel = ".".join([
                        str(x) if isinstance(x, primitive_types) else error_channel_not_primitive_type()
                        for x in channel
                    ])
            else:
                error_channel_not_primitive_type()

        if channel is None or channel == "":
            return output_path
        else:
            return f"{output_path}.{channel}"

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
