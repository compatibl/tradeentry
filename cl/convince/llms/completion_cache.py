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

import os
from dataclasses import dataclass
from typing import Any
from typing import ClassVar
from typing import Dict
from typing_extensions import Self
from cl.runtime.settings.settings import Settings
from cl.runtime.testing.stack_util import StackUtil

_supported_extensions = ["csv"]
"""The list of supported output file extensions (formats)."""


def _error_extension_not_supported(ext: str) -> Any:
    raise RuntimeError(
        f"Extension {ext} is not supported by CompletionCache. "
        f"Supported extensions: {', '.join(_supported_extensions)}"
    )


@dataclass(slots=True, init=False)
class CompletionCache:
    """
    Cache LLM completions for reducing AI cost (disable when testing the LLM itself)

    Notes:
        - After each model call, input and output are recorded in 'completions.channel.csv'
        - The channel may be based on llm_id or include some of all of the LLM settings or their hash
        - If exactly the same input is subsequently found in the completions file, it is used without calling the LLM
        - To record a new completions file, delete the existing one
    """

    __cache_dict: ClassVar[Dict[str, Self]] = {}  # TODO: Set using ContextVars
    """Dictionary of the existing CompletionCache objects indexed by '{output_dir}.{ext}'."""

    __delegate_to: Self | None
    """Delegate all function calls to this completion cache if set."""

    output_path: str  # TODO: Make private?
    """Output path including directory and llm_id."""

    ext: str
    """Output file extension (format), defaults to '.csv'"""

    __completion_dict: Dict[str, str]  # TODO: Set using ContextVars
    """Dictionary of completions indexed by query."""

    def __init__(self, *, channel: str = None, ext: str = None):
        """
        Initialize the completion cache.

        Args:
            channel: Dot-delimited string or an iterable of dot-delimited tokens to uniquely identify the cache
            ext: File extension (format) without the dot prefix, defaults to 'txt'
        """
        if channel is None or channel == "":
            raise RuntimeError("Completion cache channel is empty or None.")

        # Find base_path=dir_path/test_module by examining call stack for test function signature test_*
        base_path = StackUtil.get_base_path(allow_missing=True)

        # If not found, use base path relative to project root
        if base_path is None:
            project_root = Settings.get_project_root()
            base_path = os.path.join(project_root, "completions", "completions")

        if ext is not None:
            # Remove dot prefix if specified
            ext = ext.removeprefix(".")
            if ext not in _supported_extensions:
                _error_extension_not_supported(ext)
        else:
            # Use txt if not specified
            ext = "csv"

        # Add channel to base path if specified
        output_path = f"{base_path}.{channel}"

        # Check if completion cache already exists for the same combination of output_path and ext
        dict_key = f"{output_path}.{ext}"
        if (existing_dict := self.__cache_dict.get(dict_key, None)) is not None:
            # Delegate to the existing guard if found, do not initialize other fields
            self.__delegate_to = existing_dict
        else:
            # Otherwise add self to dictionary
            self.__cache_dict[dict_key] = self

            # Initialize fields
            self.__delegate_to = None
            self.output_path = output_path
            self.ext = ext
            self.__completion_dict = {}

    def write(self, query: str, completion: str) -> None:
        """Add new completion, will take precedence for lookup but both will be in the completions file."""

        # Delegate to a previously created guard with the same combination of output_path and ext if exists
        if self.__delegate_to is not None:
            self.__delegate_to.write(query, completion)
            return

        if self.ext == "csv":
            with open(self._get_completions_path(), "a") as file:
                formatted_query = self._format_csv(query)
                formatted_completion = self._format_csv(completion)

                # Write and flush immediately to ensure all of the output is on disk in the event of exception
                file.write(f"{formatted_query},{formatted_completion}\n")
                file.flush()

                # Add to dictionary
                self.__completion_dict[query] = completion
        else:
            # Should not be reached here because of a previous check in __init__
            _error_extension_not_supported(self.ext)

    def lookup(self, query: str) -> str | None:
        """Return completion for the specified query if found, or None otherwise."""

        # Delegate to a previously created guard with the same channel if exists
        if self.__delegate_to is not None:
            return self.lookup(query)

        cache_path = self._get_completions_path()
        if not os.path.exists(cache_path):
            # Completion cache file does not exist, return
            return None

        with open(cache_path, "r") as received_file:
            received_lines = received_file.readlines()

    def _format_csv(self, value: str) -> str:
        """Format text for CSV file (escape commas, etc.)."""
        return value

    def _get_completions_path(self) -> str:
        """The output is written to 'channel.completions.ext' in 'output_path'."""
        return f"{self.output_path}.completions.{self.ext}"
