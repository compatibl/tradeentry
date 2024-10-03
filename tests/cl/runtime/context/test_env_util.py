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
import os
from cl.runtime.context.env_util import EnvUtil


def _test_env_dir_and_name(*, expected_name: str):
    """Test for EnvUtil.env_dir and EnvUtil.env_name."""
    dir_name = os.path.dirname(__file__)
    expected_dir = os.path.join(dir_name, expected_name.replace(".", os.sep))
    assert EnvUtil.get_env_name() == expected_name
    assert os.path.normpath(EnvUtil.get_env_dir()) == os.path.normpath(expected_dir)


def test_env_util():
    """Method name matches module name, shortened path"""
    _test_env_dir_and_name(expected_name="test_env_util")


def test_in_function():
    """Function name does not match module name, two-token path."""
    _test_env_dir_and_name(expected_name="test_env_util.test_in_function")


class TestClass:
    """Stub pytest class."""

    def test_env_util(self):
        """Method name matches module name, still three-token path as they are not next to each other."""
        _test_env_dir_and_name(expected_name="test_env_util.test_class.test_env_util")

    def test_in_method(self):
        """Method name does not match class name or module name, three-token path"""
        _test_env_dir_and_name(expected_name="test_env_util.test_class.test_in_method")


class TestEnvUtil:
    """Stub pytest class with name matching the module."""

    def test_env_util(self):
        """All three match, one-token path."""
        """Method name matches module name, still three-token path as they are not next to each other."""
        _test_env_dir_and_name(expected_name="test_env_util")

    def test_in_method(self):
        """Method name does not match class name or module name which match, two-token path"""
        _test_env_dir_and_name(expected_name="test_env_util.test_in_method")


if __name__ == "__main__":
    pytest.main([__file__])
