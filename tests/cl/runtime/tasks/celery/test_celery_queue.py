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
from cl.runtime.testing.unit_test_context import UnitTestContext
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.tasks.celery.celery_queue import CeleryQueue
from cl.runtime.tasks.celery.celery_queue import execute_task
from cl.runtime.tasks.static_method_task import StaticMethodTask
from cl.runtime.tasks.task import Task
from cl.runtime.testing.celery_fixtures import celery_test_queue_fixture
from cl.runtime.testing.celery_fixtures import check_task_run_completion
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers

context_serializer = DictSerializer()
"""Serializer for the context parameter of 'execute_task' method."""


def _create_task(task_id: str) -> Task:
    """Create a test task."""

    method_callable = StubHandlers.static_handler_1a
    result = StaticMethodTask.create(task_id=task_id, record_type=StubHandlers, method_callable=method_callable)
    return result


def test_method(celery_test_queue_fixture):
    """Test calling 'execute_task' method in-process."""

    with UnitTestContext() as context:
        # Create task
        task_id = f"test_celery_queue.test_method"
        queue_id = f"test_celery_queue.test_method"
        task = _create_task(task_id)
        context.save_one(task)

        # Create task run identifier and convert to string
        task_run_uuid = OrderedUuid.create_one()
        task_run_id = str(task_run_uuid)

        # Call 'execute_task' method in-process
        context_data = context_serializer.serialize_data(context)
        execute_task(
            task_run_id,
            task_id,
            queue_id,
            context_data,
        )


def test_api(celery_test_queue_fixture):
    """Test submitting task for execution out of process."""

    with UnitTestContext() as context:
        # Create task
        task_id = f"test_celery_queue.test_api"
        queue_id = f"test_celery_queue.test_api"
        task = _create_task(task_id)
        queue = CeleryQueue(queue_id=queue_id)
        context.save_one(queue)

        # Submit task and check for its completion
        task_run_key = queue.submit_task(task)
        check_task_run_completion(task_run_key)


if __name__ == "__main__":
    pytest.main([__file__])
