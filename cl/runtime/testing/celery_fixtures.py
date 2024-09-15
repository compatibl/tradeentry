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
import datetime as dt
import time
from cl.runtime import Context
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.tasks.celery.celery_queue import celery_delete_existing_tasks
from cl.runtime.tasks.celery.celery_queue import celery_start_queue
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_run_key import TaskRunKey
from cl.runtime.tasks.task_status import TaskStatus


@pytest.fixture(scope="session")
def celery_test_queue_fixture():
    """Pytest session fixture to start Celery test queue for test execution."""
    print("Starting celery workers, will delete the existing tasks.")
    celery_delete_existing_tasks()
    celery_start_queue()  # TODO: Make test celery a separate queue
    yield
    celery_delete_existing_tasks()
    print("Stopping celery workers and cleaning up tasks.")


# TODO: Move this check out of testing?
def check_task_run_completion(task_run_key: TaskRunKey) -> None:
    """Check for completion of the task run, allowing for the delay in queue execution with the specified timeout."""

    # Get current context
    context = Context.current()

    timeout_sec = 10
    start_datetime = DatetimeUtil.now()
    while DatetimeUtil.now() < start_datetime + dt.timedelta(seconds=timeout_sec):
        task_run = context.load_one(TaskRun, task_run_key)
        if task_run is not None and task_run.status == TaskStatus.Completed:
            # Test success, task has been completed
            return
        time.sleep(1)  # Sleep for 1 second to reduce CPU load

    # Test failure
    raise RuntimeError(f"Task has not been completed after {timeout_sec} sec.")
