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

import pytest
from cl.runtime.exceptions.error_util import ErrorUtil
from cl.runtime.testing.regression_guard import RegressionGuard


def test_value_error():
    """Test for ErrorUtil.value_error method."""
    guard = RegressionGuard()
    guard.write(ErrorUtil.value_error(value=123))
    guard.write(ErrorUtil.value_error(value=123, value_name="sample_value_name"))
    guard.write(
        ErrorUtil.value_error(value=123, value_name="sample_value_name", method_name="sample_function",)
    )
    guard.write(ErrorUtil.value_error(value=123, method_name="sample_function"))
    guard.write(
        ErrorUtil.value_error(value=123, method_name="sample_method", data_type="SampleRecord",)
    )
    guard.write(
        ErrorUtil.value_error(
            value=123, value_name="sample_value_name", method_name="sample_method", data_type="SampleRecord",
        )
    )
    guard.verify()


def test_of_field():
    """Test for ErrorUtil._of_field method."""
    guard = RegressionGuard()
    assert ErrorUtil._of_field() == ""
    guard.write(ErrorUtil._of_field(field_name="sample_field"))
    guard.write(ErrorUtil._of_field(field_name="sample_field", data_type="SampleRecord"))
    guard.write(ErrorUtil._of_field(data_type="SampleRecord"))
    guard.verify()


def test_of_param():
    """Test for ErrorUtil._of_param method."""
    guard = RegressionGuard()
    assert ErrorUtil._of_param() == ""
    guard.write(ErrorUtil._of_param(param_name="sample_param"))
    guard.write(ErrorUtil._of_param(param_name="sample_param", method_name="sample_function"))
    guard.write(ErrorUtil._of_param(method_name="sample_function"))
    guard.write(ErrorUtil._of_param(method_name="sample_method", data_type="SampleRecord"))
    guard.write(
        ErrorUtil._of_param(param_name="sample_param", method_name="sample_method", data_type="SampleRecord")
    )
    guard.verify()


if __name__ == "__main__":
    pytest.main([__file__])
