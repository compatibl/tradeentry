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

from cl.runtime.context.env_util import EnvUtil


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
        test_function_pattern: str | None = None,
    ) -> str | None:
        """
        Return dot-delimited test name in 'module.test_function' or 'module.test_class.test_method' format,
        collapsing levels with identical name into one.

        Args:
            test_function_pattern: Glob pattern for function or method in stack frame, defaults to 'test_*'
        """

        # Performs stack introspection
        result = EnvUtil.get_env_name(test_function_pattern=test_function_pattern)
        return result
