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
import unittest
import inspect


def get_test_info():
    stack = inspect.stack()
    for frame_info in stack:
        if frame_info.function.startswith('test_'):
            frame_globals = frame_info.frame.f_globals
            module_name = frame_globals['__name__']
            module_file = frame_globals['__file__']
            test_name = frame_info.function
            cls_instance = frame_info.frame.f_locals.get('self', None)
            class_name = cls_instance.__class__.__name__ if cls_instance else None
            return module_file, module_name, class_name, test_name
    return None, None, None, None


def inner_function():

    file_name, module_name, class_name, test_name = get_test_info()
    print(f"File: {file_name} Module: {module_name}, Class: {class_name}, Test: {test_name}")


def test_stub_function():
    file_name, module_name, class_name, test_name = get_test_info()
    print(f"File: {file_name} Module: {module_name}, Class: {class_name}, Test: {test_name}")

    # Test calling 'get_test_info' from an inner function
    inner_function()


class TestStubClass:
    def test_stub_method(self):

        file_name, module_name, class_name, test_name = get_test_info()
        print(f"File: {file_name} Module: {module_name}, Class: {class_name}, Test: {test_name}")

        # Test calling 'get_test_info' from an inner function
        inner_function()


class TestUnitTest(unittest.TestCase):

    def test_unittest_method(self):

        file_name, module_name, class_name, test_name = get_test_info()
        print(f"File: {file_name} Module: {module_name}, Class: {class_name}, Test: {test_name}")

        # Test calling 'get_test_info' from an inner function
        inner_function()


if __name__ == "__main__":
    pytest.main([__file__])

    # Run unittest tests
    unittest.main()
