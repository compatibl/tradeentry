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

import csv
import os
from dataclasses import dataclass
from typing import Any
from typing import Dict
from uuid import UUID

from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.settings.settings import Settings
from cl.runtime.testing.stack_util import StackUtil

_supported_extensions = ["csv"]
"""The list of supported output file extensions (formats)."""

_csv_headers = ["OrderedUuid", "Timestamp", "Query", "Completion"]
"""CSV column headers."""


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
        - After each model call, input and output are recorded in 'channel.completions.csv'
        - The channel may be based on llm_id or include some of all of the LLM settings or their hash
        - If exactly the same input is subsequently found in the completions file, it is used without calling the LLM
        - To record a new completions file, delete the existing one
    """

    output_path: str
    """Output file path including directory and channel."""

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
        base_path = StackUtil.get_base_dir(allow_missing=True)

        # If not found, use base path relative to project root
        if base_path is None:
            project_root = Settings.get_project_root()
            base_path = os.path.join(project_root, "completions")

        if ext is not None:
            # Remove dot prefix if specified
            ext = ext.removeprefix(".")
            if ext not in _supported_extensions:
                _error_extension_not_supported(ext)
        else:
            # Use txt if not specified
            ext = "csv"

        # Add channel to base path to get output path
        self.output_path = f"{base_path}.{channel}.completions.{ext}"
        self.ext = ext
        self.__completion_dict = {}

        # Load cache file from disk
        self.load_cache_file()

    def add(self, query: str, completion: str) -> None:
        """Add to file even if already exits, the latest will take precedence during lookup."""

        is_new = not os.path.exists(self.output_path)
        if self.ext == "csv":
            with open(self.output_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar="\\")

                if is_new:
                    # Write the headers if the file is new
                    writer.writerow(_csv_headers)

                # NOT ADDING THE VALUE TO COMPLETION DICT HERE IS NOT A BUG
                # Because we are not adding to the dict here but only writing to a file,
                # the model will not reuse cached completions within the same session,
                # preventing incorrect measurement of stability

                # Write the new completion without checking if one already exists
                ordered_uid = OrderedUuid.create_one()
                timestamp = OrderedUuid.datetime_of(ordered_uid)
                ordered_uid_str = str(ordered_uid)
                timestamp_str = DatetimeUtil.to_str(timestamp)
                writer.writerow([ordered_uid_str, timestamp_str, query, completion])

                # Flush immediately to ensure all of the output is on disk in the event of exception
                file.flush()
        else:
            # Should not be reached here because of a previous check in __init__
            _error_extension_not_supported(self.ext)

    def get(self, query: str) -> str | None:
        """Return completion for the specified query if found and None otherwise."""
        result = self.__completion_dict.get(query, None)
        return result

    def load_cache_file(self) -> None:
        """Load cache file."""
        if os.path.exists(self.output_path):
            # Populate the dictionary from file if exists but not yet loaded
            with open(self.output_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=",", quotechar='"', escapechar="\\")

                # Read and validate the headers
                headers_in_file = next(reader, None)
                if headers_in_file != _csv_headers:
                    max_len = 20
                    headers_in_file = [h if len(max_len) < 10 else f"{h[:max_len]}..." for h in headers_in_file]
                    headers_in_file_str = ", ".join(headers_in_file)
                    expected_headers_str = ", ".join(_csv_headers)
                    raise ValueError(
                        f"Expected column headers in completions cache are {expected_headers_str}. "
                        f"Actual headers: {headers_in_file_str}."
                    )

                # Read cached completions
                row_idx = 0
                for row in reader:
                    row_idx = row_idx + 1
                    if len(row) == 4:
                        _, _, query, completion = row
                        self.__completion_dict[query] = completion
                    else:
                        raise RuntimeError(
                            f"Fewer than than 4 columns in row={row_idx} of completions cache file {self.output_path}."
                        )
