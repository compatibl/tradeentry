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
from cl.runtime.log.log import Log
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.settings.context_settings import ContextSettings
from cl.runtime.settings.settings import is_inside_test
from cl.runtime.storage.dataset_util import DatasetUtil
from cl.runtime.testing.unit_test_util import UnitTestUtil


@dataclass(slots=True, kw_only=True)
class UnitTestContext(Context):
    """
    Utilities for both pytest and unittest.

    Notes:
        - The name UnitTestUtil was selected to avoid Test prefix and does not indicate it is for unittest package only
        - This module not itself import pytest or unittest package
    """

    data_source_class: str | None = None
    """Override for the data source class in module.ClassName format."""

    def __post_init__(self):
        """Configure fields that were not specified in constructor."""

        # Do not execute this code on deserialized context instances (e.g. when they are passed to a task queue)
        if not self.is_deserialized:
            # Confirm we are inside a test, error otherwise
            if not is_inside_test:
                raise RuntimeError(f"UnitTestContext created outside a test.")

            # Get test name in 'module.test_function' or 'module.TestClass.test_method' format inside a test
            context_settings = ContextSettings.instance()

            # Use test name in dot-delimited format for context_id unless specified by the caller
            if self.context_id is None:
                test_name = UnitTestUtil.get_test_name()
                self.context_id = test_name

            # TODO: Set log field here explicitly instead of relying on implicit detection of test environment
            log_type = ClassInfo.get_class_type(context_settings.log_class)
            self.log = log_type(log_id=self.context_id)

            # Use data source class from settings unless this class provides an override
            if self.data_source_class is not None:
                data_source_class = self.data_source_class
            else:
                data_source_class = context_settings.data_source_class

            # Use 'temp' followed by context_id converted to semicolon-delimited format for data_source_id
            data_source_id = "temp;" + self.context_id.replace(".", ";")

            # Instantiate a new data source object for every test
            data_source_type = ClassInfo.get_class_type(data_source_class)
            self.data_source = data_source_type(data_source_id=data_source_id)

            # Root dataset
            self.dataset = DatasetUtil.root()

    def __enter__(self):
        """Supports 'with' operator for resource disposal."""

        # Call '__enter__' method of base first
        Context.__enter__(self)

        # Do not execute this code on deserialized context instances (e.g. when they are passed to a task queue)
        if not self.is_deserialized:
            # Delete all existing data in temp data source and drop DB in case it was not cleaned up
            # due to abnormal termination of the previous test run
            self.data_source.delete_all_and_drop_db()  # noqa

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Supports 'with' operator for resource disposal."""

        # Do not execute this code on deserialized context instances (e.g. when they are passed to a task queue)
        if not self.is_deserialized:
            # Delete all data in temp data source and drop DB to clean up
            self.data_source.delete_all_and_drop_db()  # noqa

        # Call '__exit__' method of base last
        return Context.__exit__(self, exc_type, exc_val, exc_tb)
