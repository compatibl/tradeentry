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

    __guard_dict: ClassVar[Dict[str, RegressionGuard]] = {}  # TODO: Set using ContextVars
    """Dictionary of existing guards indexed by the combination of output_dir and ext."""

    __context_stack: ClassVar[List[RegressionGuard]] = []  # TODO: Set using ContextVars
    """New current guard is pushed to the stack using 'with RegressionGuard(...)' clause."""

    __delegate_to: RegressionGuard | None
    """Delegate all function calls to this regression guard if set."""

    __verified: bool
    """Verify method sets this flag to true, after which further writes raise an error."""

    output_path: str
    """Output path including directory and channel."""

    ext: str
    """Output file extension, defaults to '.txt'"""

    def __init__(
            self,
            *,
            ext: str = None,
            channel: str | Iterable[str] | None = None,
            test_pattern: str | None = None):
        """
        Initialize the regression guard, optionally specifying channel.

        Args:
            ext: File extension without the dot prefix, defaults to 'txt'
            channel: Dot-delimited string or an iterable of dot-delimited tokens added to the current channel
            test_pattern: Glob pattern to identify the test function or method in stack frame, defaults to 'test_*'
        """

        # Check if current regression guard is set
        if len(self.__context_stack) == 0:
            # Current regression guard is not set, set output path by examining call stack
            output_path = self._get_base_path(test_pattern)
        else:
            # Set output path to the same value as the current regression guard
            current_guard = self.current()
            output_path = current_guard.output_path
            # Same for extension but only if not specified as parameter
            if ext is None:
                ext = current_guard.ext

        # Convert to string channel if specified
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

        # Add channel to output path
        if channel is not None and channel != "":
            output_path = f"{output_path}.{channel}"

        if ext is not None:
            # Remove dot prefix if specified
            ext = ext.removeprefix(".")
            if ext not in supported_extensions:
                error_extension_not_supported(ext)
        else:
            # Use txt if not specified and not obtained from the current regression guard
            ext = "txt"

        # Check if regression guard already exists for the same combination of output_path and ext
        dict_key = f"{output_path}.{ext}"
        if (existing_dict := self.__guard_dict.get(dict_key, None)) is not None:
            # Delegate to the existing guard if found, do not initialize other fields
            self.__delegate_to = existing_dict
        else:
            # Otherwise add self to dictionary
            self.__guard_dict[dict_key] = self

            # Initialize fields
            self.__delegate_to = None
            self.__verified = False
            self.output_path = output_path
            self.ext = ext

            # Delete the existing received file if exists
            if os.path.exists(received_path := self._get_received_path()):
                os.remove(received_path)

    def write(self, value: Any) -> None:
        """
        Record the argument for regression testing purposes.

        Args:
            value: Data to be recorded, accepted data types depend on the specified file extension
        """

        # Delegate to a previously created guard with the same combination of output_path and ext if exists
        if self.__delegate_to is not None:
            self.__delegate_to.write(value)
            return

        if self.__verified:
            raise RuntimeError(f"Regression output file {self._get_received_path()} is already verified "
                               f"and can no longer be written to.")

        if self.ext == "txt":
            with open(self._get_received_path(), 'a') as file:
                file.write(self._format_txt(value))
                # Flush immediately to ensure all of the output is on disk in the event of test exception
                file.flush()
        else:
            # Should not be reached here because of a previous check in __init__
            error_extension_not_supported(self.ext)

    def verify(self) -> None:
        """
        Verify for this regression guard that 'channel.received.ext' is the same as 'channel.expected.ext',
        or if 'channel.expected.ext' does not exist, copy the data from 'channel.received.ext'.
        """

        # Delegate to a previously created guard with the same combination of output_path and ext if exists
        if self.__delegate_to is not None:
            self.__delegate_to.verify()
            return

        if self.__verified:
            # Already verified, exit
            return
        else:
            # Otherwise set 'verified' flag
            self.__verified = True

        received_path = self._get_received_path()
        expected_path = self._get_expected_path()

        if os.path.exists(expected_path):
            # Expected file exists, compare
            if filecmp.cmp(received_path, expected_path, shallow=False):
                # Delete the received file if received and expected match
                os.remove(received_path)
            else:
                # Otherwise keep both files and raise an exception with unified diff
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

            # Delete the received file
            os.remove(received_path)

    @classmethod
    def verify_all(cls) -> None:
        """
        Verify for all regression guards that 'channel.received.ext' is the same as 'channel.expected.ext',
        or if 'channel.expected.ext' does not exist, copy the data from 'channel.received.ext'.
        """
        for guard in cls.__guard_dict.values():
            guard.verify()

    @classmethod
    def current(cls):
        """Return the current regression guard, error message if not set."""
        if len(cls.__context_stack) > 0:
            return cls.__context_stack[-1]
        else:
            raise RuntimeError("Current regression guard has not been set, use 'with RegressionGuard(...)' to set.")

    def __enter__(self):
        """Supports `with` operator for resource disposal."""

        # Set current guard on entering 'with RegressionGuard(...)' clause
        self.__context_stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Supports `with` operator for resource disposal."""

        # Verify only if there is no exception
        if exc_type is None:

            # Verify self
            self.verify()

            # Restore the previous current guard on exiting from 'with RegressionGuard(...)' clause
            if len(self.__context_stack) > 0:
                current_guard = self.__context_stack.pop()
            else:
                if exc_type is None:
                    raise RuntimeError("Current regression guard is cleared inside 'with RegressionGuard(...)' clause.")

            if current_guard is not self:
                if exc_type is None:
                    raise RuntimeError("Current regression guard is modified inside 'with RegressionGuard(...)' clause.")

        # Return False to propagate the exception to the caller
        return False
        
    def _format_txt(self, value: Any) -> str:
        """Format text for regression testing."""
        value_type = type(value)
        if value_type in primitive_types:
            # TODO: Use specialized conversion for primitive types
            return str(value) + "\n"
        elif value_type == dict:
            return yaml.dump(value, default_flow_style=False) + "\n"
        elif hasattr(value_type, "__iter__"):
            return "\n".join(map(self._format_txt, value)) + "\n"
        else:
            raise RuntimeError(f"Argument type {value_type} is not accepted for file extension '{self.ext}'. "
                               f"Valid arguments are primitive types, dict, or their iterable.")

    def _get_received_path(self) -> str:
        """The output is recorded in 'channel.received.ext' located next to the unit test."""
        return f"{self.output_path}.received.{self.ext}"

    def _get_expected_path(self) -> str:
        """The output is compared to 'channel.expected.ext' located next to the unit test."""
        return f"{self.output_path}.expected.{self.ext}"

    @classmethod
    def _get_base_path(cls, test_pattern: str | None = None) -> str:
        """
        Return test_module.test_function or test_module.test_class.test_function  by searching the stack frame
        for 'test_' or a custom test function name pattern.

        Args:
            test_pattern: Glob pattern to identify the test function or method in stack frame, defaults to 'test_*'
        """

        if test_pattern is not None:
            # TODO: Support custom patterns
            raise RuntimeError("Custom test function or method name patterns are not yet supported.")

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
