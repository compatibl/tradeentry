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

import difflib
import filecmp
import inspect
import os
from dataclasses import dataclass
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Iterable
from typing import cast
import inflection
import yaml
from typing_extensions import Self
from cl.runtime.records.protocols import is_key
from cl.runtime.records.protocols import is_record
from cl.runtime.schema.field_decl import primitive_types
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.testing.stack_util import StackUtil

_supported_extensions = ["txt"]
"""The list of supported output file extensions (formats)."""

key_serializer = StringSerializer()
"""Serializer for keys."""

data_serializer = DictSerializer()
"""Serializer for records."""


def _error_channel_not_primitive_type() -> Any:
    raise RuntimeError("Output channel must be a primitive type or an iterable of primitive types.")


def _error_extension_not_supported(ext: str) -> Any:
    raise RuntimeError(
        f"Extension {ext} is not supported by RegressionGuard. "
        f"Supported extensions: {', '.join(_supported_extensions)}"
    )


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

    __guard_dict: ClassVar[Dict[str, Self]] = {}  # TODO: Set using ContextVars
    """Dictionary of existing guards indexed by the combination of output_dir and ext."""

    __delegate_to: Self | None
    """Delegate all function calls to this regression guard if set."""

    __verified: bool
    """Verify method sets this flag to true, after which further writes raise an error."""

    __exception_text: str | None
    """Exception text from an earlier verification is reused instead of comparing the files again."""

    output_path: str
    """Output path including directory and channel."""

    ext: str
    """Output file extension (format), defaults to '.txt'"""

    def __init__(
        self, *, ext: str = None, channel: str | Iterable[str] | None = None, test_function_pattern: str | None = None
    ):
        """
        Initialize the regression guard, optionally specifying channel.

        Args:
            ext: File extension (format) without the dot prefix, defaults to 'txt'
            channel: Dot-delimited string or an iterable of dot-delimited tokens added to the current channel
            test_function_pattern: Glob pattern to identify the test function or method in stack frame, defaults to 'test_*'
        """

        # Convert channel to string from other types
        if channel is not None:
            if isinstance(channel, primitive_types):  # TODO: Move primitive_types to another module
                # TODO: Use specialized conversion for primitive types
                channel = str(channel)
            elif hasattr(channel, "__iter__"):
                # TODO: Use specialized conversion for primitive types
                channel = ".".join(
                    [str(x) if isinstance(x, primitive_types) else _error_channel_not_primitive_type() for x in channel]
                )
            else:
                _error_channel_not_primitive_type()

        # Find base path by examining call stack
        base_path = StackUtil.get_base_path(test_function_pattern=test_function_pattern)

        # Add channel to base path if specified
        if channel is not None and channel != "":
            output_path = f"{base_path}.{channel}"
        else:
            output_path = base_path

        if ext is not None:
            # Remove dot prefix if specified
            ext = ext.removeprefix(".")
            if ext not in _supported_extensions:
                _error_extension_not_supported(ext)
        else:
            # Use txt if not specified
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
            self.__exception_text = None
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
            raise RuntimeError(
                f"Regression output file {self._get_received_path()} is already verified "
                f"and can no longer be written to."
            )

        if self.ext == "txt":
            with open(self._get_received_path(), "a") as file:
                file.write(self._format_txt(value))
                # Flush immediately to ensure all of the output is on disk in the event of test exception
                file.flush()
        else:
            # Should not be reached here because of a previous check in __init__
            _error_extension_not_supported(self.ext)

    @classmethod
    def verify_all(cls, *, silent: bool = False) -> None:
        """
        For each created guard, verify that 'channel.received.ext' is the same as 'channel.expected.ext'.
        Defaults to silent=False (raises exception) for calling at the end of the test.

        Notes:
            - If 'channel.expected.ext' does not exist, create from 'channel.received.ext'
            - If files are the same, delete 'channel.received.ext' and 'channel.diff.ext'
            - If files differ, write 'channel.diff.ext' and optionally raise exception

        Args:
            silent: If true, write the diff file but do not raise exception
        """

        # Call verify for all guards silently and check if all are true
        # Because 'all' is used, the comparison will not stop early
        errors_found = not all(guard.verify(silent=True) for guard in cls.__guard_dict.values())

        if errors_found and not silent:
            # Collect exception text from guards where it is present
            exc_text_blocks = [
                exception_text
                for guard in cls.__guard_dict.values()
                if (exception_text := guard._get_exception_text()) is not None
            ]

            # Merge the collected exception text blocks and raise an error
            exc_text_merged = "\n".join(exc_text_blocks)
            raise RuntimeError(exc_text_merged)

    def verify(self, *, silent: bool = True) -> bool:
        """
        Verify for this regression guard that 'channel.received.ext' is the same as 'channel.expected.ext'.
        Defaults to silent=True (no exception) to permit other tests to proceed.

        Notes:
            - If 'channel.expected.ext' does not exist, create from 'channel.received.ext'
            - If files are the same, delete 'channel.received.ext' and 'channel.diff.ext'
            - If files differ, write 'channel.diff.ext' and raise exception unless silent=True

        Returns:
            bool: True if verification succeeds and false otherwise

        Args:
            silent: If true, do not raise exception and only write the 'channel.diff.ext' file
        """

        # Delegate to a previously created guard with the same combination of output_path and ext if exists
        if self.__delegate_to is not None:
            return self.verify(silent=silent)

        if self.__verified:
            # Already verified
            if not silent:
                # Use the existing exception text to raise if silent=False
                raise RuntimeError(self.__exception_text)
            else:
                # Otherwise return True if exception text is None (it is set on verification failure)
                return self.__exception_text is None
        else:
            # Otherwise set 'verified' flag and continue
            self.__verified = True

        received_path = self._get_received_path()
        expected_path = self._get_expected_path()
        diff_path = self._get_diff_path()

        if not os.path.exists(received_path):
            raise RuntimeError(f"Regression test error, received file {received_path} does not exist.")

        if os.path.exists(expected_path):
            # Expected file exists, compare
            if filecmp.cmp(received_path, expected_path, shallow=False):
                # Received and expected match, delete the received file and diff file
                os.remove(received_path)
                if os.path.exists(diff_path):
                    os.remove(diff_path)

                # Return True to indicate verification has been successful
                return True
            else:
                # Receive an expected do not match, generate unified diff
                # TODO: Handle diff for binary output
                with open(received_path, "r") as received_file:
                    received_lines = received_file.readlines()
                with open(expected_path, "r") as expected_file:
                    expected_lines = expected_file.readlines()

                # Convert to list first because the returned object is a generator but
                # we will need to iterate over the lines more than once
                diff = list(
                    difflib.unified_diff(
                        expected_lines, received_lines, fromfile=expected_path, tofile=received_path, n=0
                    )
                )

                # Write the complete unified diff into to the diff file
                with open(diff_path, "w") as diff_file:
                    diff_file.write("".join(diff))

                # Truncate to max_lines and surround by begin/end lines for generate exception text
                line_len = 120
                max_lines = 5
                begin_str = "BEGIN REGRESSION TEST UNIFIED DIFF "
                end_str = "END REGRESSION TEST UNIFIED DIFF "
                begin_sep = "-" * (line_len - len(begin_str))
                end_sep = "-" * (line_len - len(end_str))
                orig_lines = len(diff)
                if orig_lines > max_lines:
                    diff = diff[:max_lines]
                    truncate_str = f"(TRUNCATED {orig_lines-max_lines} ADDITIONAL LINES) "
                    end_sep = end_sep[: -len(truncate_str)]
                else:
                    truncate_str = ""
                diff_str = "".join(diff)
                exception_text = f"\n{begin_str}{begin_sep}\n" + diff_str
                extra_eol = "" if exception_text.endswith("\n") else "\n"
                exception_text = exception_text + f"{extra_eol}{end_str}{truncate_str}{end_sep}"

                # Record into the object even if silent
                self.__exception_text = exception_text

                if not silent:
                    # Raise exception only when not silent
                    raise RuntimeError(exception_text)
                else:
                    return False
        else:
            # Expected file does not exist, copy the data from received to expected
            with open(received_path, "rb") as received_file, open(expected_path, "wb") as expected_file:
                expected_file.write(received_file.read())

            # Delete the received file and diff file
            os.remove(received_path)
            if os.path.exists(diff_path):
                os.remove(diff_path)

            # Verification is considered successful if expected file has been created
            return True

    def _format_txt(self, value: Any) -> str:
        """Format text for regression testing."""
        value_type = type(value)
        if value_type in primitive_types:
            # TODO: Use specialized conversion for primitive types
            return str(value) + "\n"
        elif value_type == dict:
            return yaml.dump(value, default_flow_style=False, sort_keys=False) + "\n"
        elif is_record(value_type):
            return data_serializer.serialize_data(value)
        elif is_key(value_type):
            return key_serializer.serialize_data(value)
        elif hasattr(value_type, "__iter__"):
            return "\n".join(map(self._format_txt, value)) + "\n"
        else:
            raise RuntimeError(
                f"Argument type {value_type} is not accepted for file extension '{self.ext}'. "
                f"Valid arguments are primitive types, dict, or their iterable."
            )

    def _get_exception_text(self) -> str | None:
        """Get exception text from this guard or the guard it delegates to."""
        if self.__delegate_to is not None:
            # Get from the guard this guard delegates to
            return self.__delegate_to._get_exception_text()
        else:
            # Get from this guard
            return self.__exception_text

    def _get_received_path(self) -> str:
        """The output is written to 'channel.received.ext' located next to the unit test."""
        return f"{self.output_path}.received.{self.ext}"

    def _get_expected_path(self) -> str:
        """The output is compared to 'channel.expected.ext' located next to the unit test."""
        return f"{self.output_path}.expected.{self.ext}"

    def _get_diff_path(self) -> str:
        """The diff between received and expected is written to 'channel.diff.ext' located next to the unit test."""
        return f"{self.output_path}.diff.{self.ext}"
