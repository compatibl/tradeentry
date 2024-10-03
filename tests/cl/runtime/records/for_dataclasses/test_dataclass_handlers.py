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
from cl.runtime.context.testing_context import TestingContext
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers


def test_smoke():
    """Smoke test."""

    with TestingContext():
        # Instance method handlers
        obj = StubHandlers()
        obj.run_instance_method_1a()
        obj.run_instance_method_1b()
        if False:  # TODO: Restore when handlers with parameters are available
            obj.run_instance_method_2a(param1="a")
            obj.run_instance_method_2b(param1="a")
            obj.run_instance_method_3a(param1="a", param2="b")
            obj.run_instance_method_3b(param1="a", param2="b")

        # Class method handlers
        StubHandlers.run_class_method_1a()
        StubHandlers.run_class_method_1b()
        if False:  # TODO: Restore when handlers with parameters are available
            StubHandlers.run_class_method_2a(param1="a")
            StubHandlers.run_class_method_2b(param1="a")
            StubHandlers.run_class_method_3a(param1="a", param2="b")
            StubHandlers.run_class_method_3b(param1="a", param2="b")

        # Static method handlers
        StubHandlers.run_static_method_1a()
        StubHandlers.run_static_method_1b()
        if False:  # TODO: Restore when handlers with parameters are available
            StubHandlers.run_static_method_2a(param1="a")
            StubHandlers.run_static_method_2b(param1="a")
            StubHandlers.run_static_method_3a(param1="a", param2="b")
            StubHandlers.run_static_method_3b(param1="a", param2="b")


if __name__ == "__main__":
    pytest.main([__file__])
