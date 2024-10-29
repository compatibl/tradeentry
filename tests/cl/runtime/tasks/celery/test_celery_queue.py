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
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.tasks.celery.celery_queue import CeleryQueue
from cl.runtime.tasks.celery.celery_queue import execute_task
from cl.runtime.tasks.static_method_task import StaticMethodTask
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.testing.pytest.pytest_fixtures import celery_test_queue_fixture
from stubs.cl.runtime import StubHandlers

context_serializer = DictSerializer()
"""Serializer for the context parameter of 'execute_task' method."""


def _create_task() -> TaskKey:
    """Create a test task."""

    method_callable = StubHandlers.run_static_method_1a
    task = StaticMethodTask.create(record_type=StubHandlers, method_callable=method_callable)
    Context.current().save_one(task)
    return task.get_key()


@pytest.mark.skip("Celery tasks lock sqlite db file.")  # TODO (Roman): resolve conflict
def test_method(celery_test_queue_fixture):
    """Test calling 'execute_task' method in-process."""

    with TestingContext() as context:
        # Create task
        queue_id = f"test_celery_queue.test_method"
        task_key = _create_task()

        # Call 'execute_task' method in-process
        context_data = context_serializer.serialize_data(context)
        execute_task(
            task_key.task_id,
            context_data,
        )


@pytest.mark.skip("Celery tasks lock sqlite db file.")  # TODO (Roman): resolve conflict
def test_api(celery_test_queue_fixture):
    """Test submitting task for execution out of process."""

    with TestingContext() as context:
        # Create task
        queue_id = f"test_celery_queue.test_api"
        task_key = _create_task()
        queue = CeleryQueue(queue_id=queue_id)
        context.save_one(queue)

        # Submit task and check for its completion
        queue.submit_task(task_key)
        Task.wait_for_completion(task_key)


if __name__ == "__main__":
    pytest.main([__file__])
