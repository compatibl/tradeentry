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
from cl.runtime import Context
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers


def test_smoke():
    """Smoke test."""

    with Context():
        # Instance method handlers
        obj = StubHandlers()
        obj.instance_handler_1a()
        obj.instance_handler_1b()
        obj.instance_handler_2a(param1="a")
        obj.instance_handler_2b(param1="a")
        obj.instance_handler_3a(param1="a", param2="b")
        obj.instance_handler_3b(param1="a", param2="b")

        # Class method handlers
        StubHandlers.class_handler_1a()
        StubHandlers.class_handler_1b()
        StubHandlers.class_handler_2a(param1="a")
        StubHandlers.class_handler_2b(param1="a")
        StubHandlers.class_handler_3a(param1="a", param2="b")
        StubHandlers.class_handler_3b(param1="a", param2="b")

        # Static method handlers
        StubHandlers.static_handler_1a()
        StubHandlers.static_handler_1b()
        StubHandlers.static_handler_2a(param1="a")
        StubHandlers.static_handler_2b(param1="a")
        StubHandlers.static_handler_3a(param1="a", param2="b")
        StubHandlers.static_handler_3b(param1="a", param2="b")


if __name__ == "__main__":
    pytest.main([__file__])
