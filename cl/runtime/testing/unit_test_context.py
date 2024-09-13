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

from dataclasses import dataclass
from cl.runtime.context.context import Context
from cl.runtime.testing.pytest_util import UnitTestUtil


@dataclass(slots=True, kw_only=True)
class UnitTestContext(Context):
    """
    Utilities for both pytest and unittest.

    Notes:
        - The name UnitTestUtil was selected to avoid Test prefix and does not indicate it is for unittest package only
        - This module not itself import pytest or unittest package
    """

    def __post_init__(self):
        """Configure for use inside a test runner."""

        # Context identifier in 'module.test_function' or 'module.TestClass.test_method' format
        self.context_id = UnitTestUtil.get_test_name()

        # Matching dataset identifier
        self.data_source.data_source_id = self.context_id
