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
import sys


class PytestUtil:
    """Pytest-related utilities that do not import pytest module and therefore can be invoked from non-test code."""

    @classmethod
    def is_inside_pytest(cls) -> bool:
        """Return true if invoked by the pytest test runner."""
        return "pytest" in sys.modules

    @classmethod
    def get_current_pytest(cls) -> str | None:
        """Return the current pytest or None if not invoked by the pytest test runner."""
        result = os.getenv('PYTEST_CURRENT_TEST', None)
        return result

    @classmethod
    def get_caller_name(cls, *, caller_file: str) -> str:  # TODO: Use __name__ instead, review use
        """
        Get caller script name without extension from its __file__ variable.

        Use to make test input and output files begin from the prefix
        based on test .py file name.
        """

        file_path, file_name_with_ext = os.path.split(caller_file)
        file_name, file_ext = os.path.splitext(file_name_with_ext)
        return file_name
