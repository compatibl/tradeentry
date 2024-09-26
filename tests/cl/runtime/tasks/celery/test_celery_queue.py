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
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.tasks.celery.celery_queue import CeleryQueue
from cl.runtime.tasks.celery.celery_queue import execute_task
from cl.runtime.tasks.static_method_task import StaticMethodTask
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_queue_key import TaskQueueKey
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_status_enum import TaskStatusEnum
from cl.runtime.testing.pytest.pytest_fixtures import celery_test_queue_fixture
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers

context_serializer = DictSerializer()
"""Serializer for the context parameter of 'execute_task' method."""


def _create_task(task_id: str) -> Task:
    """Create a test task."""

    method_callable = StubHandlers.run_static_method_1a
    result = StaticMethodTask.create(task_id=task_id, record_type=StubHandlers, method_callable=method_callable)
    return result


@pytest.mark.skip("Celery tasks lock sqlite db file.")  # TODO (Roman): resolve conflict
def test_method(celery_test_queue_fixture):
    """Test calling 'execute_task' method in-process."""

    with TestingContext() as context:
        # Create task
        task_id = f"test_celery_queue.test_method"
        queue_id = f"test_celery_queue.test_method"
        task = _create_task(task_id)
        context.save_one(task)

        # Create task run identifier and convert to string
        task_run_uuid = OrderedUuid.create_one()
        task_run_id = str(task_run_uuid)

        submit_time = OrderedUuid.datetime_of(task_run_uuid)

        # Create a task run record in Pending state
        task_run = TaskRun()
        task_run.task_run_id = task_run_id
        task_run.queue = TaskQueueKey(queue_id="test_queue")
        task_run.task = task
        task_run.submit_time = submit_time
        task_run.update_time = submit_time
        task_run.status = TaskStatusEnum.PENDING

        # Save task run record which means task is submitted
        context.save_one(task_run)

        # Call 'execute_task' method in-process
        context_data = context_serializer.serialize_data(context)
        execute_task(
            task_run_id,
            context_data,
        )


@pytest.mark.skip("Celery tasks lock sqlite db file.")  # TODO (Roman): resolve conflict
def test_api(celery_test_queue_fixture):
    """Test submitting task for execution out of process."""

    with TestingContext() as context:
        # Create task
        task_id = f"test_celery_queue.test_api"
        queue_id = f"test_celery_queue.test_api"
        task = _create_task(task_id)
        queue = CeleryQueue(queue_id=queue_id)
        context.save_one(queue)

        # Submit task and check for its completion
        task_run_key = queue.submit_task(task)
        TaskRun.wait_for_completion(task_run_key)


if __name__ == "__main__":
    pytest.main([__file__])
