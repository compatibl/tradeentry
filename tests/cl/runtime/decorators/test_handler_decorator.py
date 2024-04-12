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

from stubs.cl.runtime.decorators.stub_handler_methods import StubHandlerMethods


def test_smoke():
    """Smoke test."""

    # Create test record and populate with sample data
    obj = StubHandlerMethods()

    obj.instance_handler_1a()
    obj.instance_handler_1b()
    obj.instance_handler_2a(param1="a")
    obj.instance_handler_2b(param1="a")
    obj.instance_handler_3a(param1="a", param2="b")
    obj.instance_handler_3b(param1="a", param2="b")

    StubHandlerMethods.class_handler_1a()
    StubHandlerMethods.class_handler_1b()
    StubHandlerMethods.class_handler_2a(param1="a")
    StubHandlerMethods.class_handler_2b(param1="a")
    StubHandlerMethods.class_handler_3a(param1="a", param2="b")
    StubHandlerMethods.class_handler_3b(param1="a", param2="b")

    StubHandlerMethods.static_handler_1a()
    StubHandlerMethods.static_handler_1b()
    StubHandlerMethods.static_handler_2a(param1="a")
    StubHandlerMethods.static_handler_2b(param1="a")
    StubHandlerMethods.static_handler_3a(param1="a", param2="b")
    StubHandlerMethods.static_handler_3b(param1="a", param2="b")


if __name__ == "__main__":
    pytest.main([__file__])
