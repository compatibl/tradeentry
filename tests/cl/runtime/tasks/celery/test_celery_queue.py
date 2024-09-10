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
from cl.runtime.tasks.celery.celery_queue import execute_task, CeleryQueue
from cl.runtime.tasks.static_method_task import StaticMethodTask
from cl.runtime.tasks.task import Task
from cl.runtime.testing.celery_testing import celery_start_test_workers
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers


def _create_task(task_id: str) -> Task:
    """Create a test task."""

    method_callable = StubHandlers.static_handler_1a
    result = StaticMethodTask.create(task_id="abc", record_type=StubHandlers, method_callable=method_callable)
    return result


def test_method(celery_start_test_workers):
    """Smoke test."""

    with Context():
        task = _create_task(f"test_celery_queue.test_method")
        Context.save_one(task)
        result_task = execute_task.delay(task.task_id)
        result_task.get(timeout=2)


def test_api(celery_start_test_workers):
    """Smoke test."""

    with Context():
        task = _create_task(f"test_celery_queue.test_api")

        queue = CeleryQueue()
        task_run_key = queue.submit_task(task)
        pass


if __name__ == "__main__":
    pytest.main([__file__])
