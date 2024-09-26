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
from cl.runtime.testing.stack_util import StackUtil


class TestingUtil:
    """
    Utilities for both pytest and unittest.

    Notes:
        - The name TestingUtil was selected to avoid Test prefix and does not indicate it is for unittest package only
        - This module not itself import pytest or unittest package and therefore can be used in non-test code
    """

    @classmethod
    def get_test_name(
        cls,
        *,
        allow_missing: bool = False,
        test_function_pattern: str | None = None,
    ) -> str | None:
        """
        Return dot-delimited test name in 'module.test_function' or 'module.TestClass.test_method' format
        by searching the stack frame for 'test_' or a custom test function name pattern.

        Args:
            allow_missing: If True, return None if path is not found (e.g. when not running inside a test)
            test_function_pattern: Glob pattern to identify the test function or method in stack frame,
            defaults to 'test_*'
        """

        # Perform stack introspection
        base_path = StackUtil.get_base_path(
            allow_missing=allow_missing,
            test_function_pattern=test_function_pattern,
        )

        if base_path is not None:
            # Result is the last token in path
            result = os.path.basename(base_path)
            return result
        else:
            # Not running inside a test, return None (if allow_missing=True, get_base_path would already raise an error)
            return None
