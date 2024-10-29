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
from cl.runtime.tasks.instance_method_task import InstanceMethodTask
from cl.runtime.tasks.task_queue_key import TaskQueueKey
from stubs.cl.runtime import StubHandlers


def test_smoke():
    """Test 'test_create' method."""

    with TestingContext() as context:
        records = [
            StubHandlers(stub_id="abc"),
        ]
        context.save_many(records)

        object_and_instance_handler_on_object = [(x, x.run_instance_method_1a) for x in records]
        key_and_instance_handler_on_object = [(x.get_key(), x.run_instance_method_1a) for x in records]
        object_and_instance_handler_on_class = [(x, StubHandlers.run_instance_method_1a) for x in records]
        key_and_instance_handler_on_class = [(x.get_key(), StubHandlers.run_instance_method_1a) for x in records]
        object_and_class_handler_on_class = [(x, StubHandlers.run_class_method_1a) for x in records]
        key_and_class_handler_on_class = [(x.get_key(), StubHandlers.run_class_method_1a) for x in records]

        sample_inputs = (
            object_and_instance_handler_on_object
            + key_and_instance_handler_on_object
            + object_and_instance_handler_on_class
            + key_and_instance_handler_on_class
            + object_and_class_handler_on_class
            + key_and_class_handler_on_class
        )

        for sample_input in sample_inputs:
            record_or_key = sample_input[0]
            method_callable = sample_input[1]
            task = InstanceMethodTask.create(
                queue=TaskQueueKey(queue_id="NoQueue"),  # The task will be executed without saving
                record_or_key=record_or_key,
                method_callable=method_callable,
            )
            task.run_task()


if __name__ == "__main__":
    pytest.main([__file__])
