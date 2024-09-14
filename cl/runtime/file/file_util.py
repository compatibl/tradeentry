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
import re

invalid_filename_symbols = r'/\\<>:"|?*'
"""Invalid filename symbols."""

invalid_filename_regex = re.compile(f"[{invalid_filename_symbols}]")
"""Precompiled regex to check for invalid filename symbols."""

invalid_path_symbols = r'<>:"|?*'
"""Precompiled regex to check for invalid filename symbols."""

invalid_path_regex = re.compile(f"[{invalid_path_symbols}]")
"""Precompiled regex to check for invalid filename symbols."""


class FileUtil:
    """Utilities for working with files."""

    @classmethod
    def check_valid_filename(cls, filename: str) -> None:
        """Error if invalid symbols are present in filename (do not use for path with directory separators)."""
        if invalid_filename_regex.search(filename):
            raise RuntimeError(f"Filename '{filename}' is not valid because it contains special characters "
                               f"from this list: {invalid_filename_symbols}")

    @classmethod
    def check_valid_path(cls, path: str) -> None:
        """Error if invalid symbols are present in directory or file path (directory separators are allowed)."""
        if invalid_path_regex.search(path):
            raise RuntimeError(f"Directory or file path '{path}' is not valid because it contains special characters "
                               f"from this list: {invalid_path_symbols}")

    @classmethod
    def has_extension(cls, path: str, ext: str | None) -> bool:
        """Return True if filename or path extension matches argument, use ext=None to return True for any extension."""
        # Get the actual extension from path
        actual_ext = os.path.splitext(path)[1]

        # Normalize both
        ext = cls.normalize_ext(ext)
        actual_ext = cls.normalize_ext(actual_ext)

        # Check for match
        return actual_ext == ext

    @classmethod
    def check_extension(cls, path: str, ext: str | None) -> None:
        """Error if filename or path extension does not match argument, use ext=None to check for any extension."""
        if not cls.has_extension(path, ext):
            # Get the actual extension from path
            actual_ext = os.path.splitext(path)[1]

            # Normalize both
            ext = cls.normalize_ext(ext)
            actual_ext = cls.normalize_ext(actual_ext)

            # Report error
            if ext is not None:
                if actual_ext is not None:
                    raise RuntimeError(f"Filename or path '{path}' has extension '{actual_ext}' which does not match "
                                       f"the expected extension '{ext}'.")
                else:
                    raise RuntimeError(
                        f"Filename or path '{path}' has no extension while extension '{ext}' should be present.")
            else:
                raise RuntimeError(
                    f"Filename or path '{path}' has extension '{actual_ext}' while no extension should be present.")

    @classmethod
    def normalize_ext(cls, ext: str) -> str | None:
        """Remove leading period if specified and convert to lowercase."""
        # Check for None or empty string
        if ext is not None and ext != "":
            result = ext if not ext.startswith(".") else ext[1:]
            result = result.lower()
            return result
        else:
            return None
