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

from cl.runtime.context.context import Context
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.settings.context_settings import ContextSettings
from cl.runtime.testing.unit_test_util import UnitTestUtil
from dataclasses import dataclass


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

        # Get test name in 'module.test_function' or 'module.TestClass.test_method' format if running inside a test
        test_name = UnitTestUtil.get_test_name(allow_missing=True)
        if test_name is not None:
            # Create a new data source for every test
            context_settings = ContextSettings.instance()
            data_source_type = ClassInfo.get_class_type(context_settings.data_source_class)

            # TODO: Add code to obtain from preloads if only key is specified
            self.data_source = data_source_type(data_source_id=test_name)
            self.context_id = self.data_source.data_source_id
