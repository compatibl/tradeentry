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
from cl.runtime.tasks.static_method_task import StaticMethodTask
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers


def test_create():
    """Test 'test_create' method."""

    with Context():
        sample_inputs = [
            (StubHandlers, StubHandlers.class_handler_1a),
            (StubHandlers, StubHandlers.static_handler_1a),
        ]

        for sample_input in sample_inputs:
            record_type = sample_input[0]
            method_callable = sample_input[1]
            task = StaticMethodTask.create(task_id="abc", record_type=record_type, method_callable=method_callable)
            task.execute()


if __name__ == "__main__":
    pytest.main([__file__])
