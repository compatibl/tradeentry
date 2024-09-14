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
from cl.runtime.log.log import Log
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.settings.context_settings import ContextSettings
from cl.runtime.settings.settings import is_inside_test
from cl.runtime.storage.dataset_util import DatasetUtil
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
        """Configure fields that were not specified in constructor."""

        # Check if the object is being deserialized, in which case fields should be obtained from serialized data
        if self.is_constructed:
            return
        else:
            self.is_constructed = True

        # Confirm we are inside a test, error otherwise
        if not is_inside_test:
            raise RuntimeError(f"UnitTestContext created outside a test.")

        # Get test name in 'module.test_function' or 'module.TestClass.test_method' format inside a test
        context_settings = ContextSettings.instance()
        test_name = UnitTestUtil.get_test_name()

        # Use test name for context_id
        self.context_id = test_name

        # TODO: Set log field here explicitly instead of relying on implicit detection of test environment
        log_type = ClassInfo.get_class_type(context_settings.log_class)
        self.log = log_type(log_id=self.context_id)

        # Create a new data source for every test, set data_source_id to context_id

        data_source_type = ClassInfo.get_class_type(context_settings.data_source_class)
        self.data_source = data_source_type(data_source_id=self.context_id)

        # Root dataset
        self.dataset = DatasetUtil.root()
