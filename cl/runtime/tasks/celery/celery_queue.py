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

import multiprocessing
import platform
from dataclasses import dataclass
from typing import Final, List, Optional, cast
from celery import Celery
from cl.runtime.primitive.ordered_uuid import OrderedUuid
from cl.runtime.records.protocols import is_record
from cl.runtime import Context
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.tasks.task_queue import TaskQueue
from cl.runtime.tasks.task_run import TaskRun
from cl.runtime.tasks.task_run_key import TaskRunKey
from cl.runtime.tasks.task_status import TaskStatus

CELERY_MAX_WORKERS = 4

CELERY_RUN_COMMAND_QUEUE: Final[str] = 'run_command'
CELERY_MAX_RETRIES: Final[int] = 3
CELERY_TIME_LIMIT: Final[int] = 3600 * 2  # TODO: 2 hours (configure)

celery_app = Celery(
    "worker",
    broker="mongodb://localhost:27017/celery",
    backend="mongodb://localhost:27017/celery",
    broker_connection_retry_on_startup=True,
)

celery_app.conf.task_track_started = True


@celery_app.task
def execute_task(task_id: str, task_run_id_str: str) -> None:
    """Invoke execute method of the specified task."""

    with Context():
        # Load task object
        task_key = TaskKey(task_id=task_id)
        task = Context.load_one(Task, task_key)
        task.execute()


@celery_app.task
def completed_task(task_id: str, task_run_id_str: str) -> None:
    raise RuntimeError()
    with Context():
        print(f"Completed {task_id}")


@celery_app.task
def error_task(task_id: str, task_run_id_str: str) -> None:
    with Context():
        print(f"Error {task_id}")


def celery_start_workers(worker_name: Optional[str] = None, queue_names: Optional[List[str]] = None) -> None:

    # Celery doesn't support prefork on Windows
    # pool = "solo" if platform.system() != 'Linux' else "prefork"
    pool = "solo"  # One concurrent task per worker
    concurrency = 1  # Only applies in case of prefork, but not in case of solo

    celery_app.worker_main(
        argv=[
            '-A',
            'cl.runtime.tasks.celery.celery_queue',
            'worker',
            '--loglevel=info',
            f'--autoscale={CELERY_MAX_WORKERS},1',
            f'--pool={pool}',
            f'--concurrency={concurrency}',  # Use only in case of prefork
        ],
    )


def celery_start_workers_process(worker_name: Optional[str] = None, queue_names: Optional[List[str]] = None) -> None:

    # Start Celery workers (will exit when the current process exits)
    worker_process = multiprocessing.Process(target=celery_start_workers, daemon=True)
    worker_process.start()


@dataclass(slots=True, kw_only=True)
class CeleryQueue(TaskQueue):
    """Submits tasks to Celery workers."""

    # max_workers: int = missing()  # TODO: Implement support for max_workers
    """The maximum number of processes running concurrently."""

    # TODO: @abstractmethod
    def start_workers(self) -> None:
        """Start queue workers."""

    # TODO: @abstractmethod
    def stop_workers(self) -> None:
        """Cancel all active runs and stop queue workers."""

    # TODO: @abstractmethod
    def cancel_all(self) -> None:
        """Cancel all active runs but do not stop queue workers."""

    # TODO: @abstractmethod
    def pause_all(self) -> None:
        """Do not start new runs and send pause command to the existing runs."""

    # TODO: @abstractmethod
    def resume_all(self) -> None:
        """Resume starting new runs and send resume command to existing runs."""

    def submit_task(self, task: TaskKey) -> TaskRunKey:
        """Submit task to this queue (all further access to the run is provided via the returned TaskRunKey)."""

        # Save task if provided as record rather than key
        if is_record(task):
            Context.save_one(task)

        # Create task run identifier and save its timestamp
        task_run_id = OrderedUuid.create_one()
        task_run_id_str = str(task_run_id)
        submit_time = OrderedUuid.datetime_of(task_run_id)

        # Task parameters for Celery
        kwargs = {"task_run_id_str": task_run_id_str}

        # Create Celery task signatures
        execute_task_signature = execute_task.s(task.task_id, task_run_id_str)
        completed_task_signature = completed_task.s(task.task_id, task_run_id_str)
        error_task_signature = error_task.s(task.task_id, task_run_id_str)

        # Submit task to Celery with completed and error links
        execute_task_signature.apply_async(
            retry=False,  # Do not retry in case the task fails
            # ignore_result=True,  # TODO: Do not publish to the Celery result backend
            link=completed_task_signature,
            link_error=error_task_signature,
        )

        # Save task run record
        task_run = TaskRun()
        task_run.task_run_id = task_run_id
        task_run.queue = self.get_key()
        task_run.task = task
        task_run.submit_time = submit_time
        task_run.update_time = submit_time
        task_run.status = TaskStatus.Completed  # TODO: Update after the task is actually completed
        Context.save_one(task_run)

        return task_run.get_key()

