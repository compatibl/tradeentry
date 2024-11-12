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
import os
from dataclasses import dataclass
from typing import Final
from uuid import UUID
from celery import Celery
from cl.runtime import Context
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.log.log_entry import LogEntry
from cl.runtime.log.log_entry_level_enum import LogEntryLevelEnum
from cl.runtime.log.user_log_entry import UserLogEntry
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.records.protocols import TDataDict
from cl.runtime.records.protocols import is_key
from cl.runtime.records.protocols import is_record
from cl.runtime.serialization.dict_serializer import DictSerializer
from cl.runtime.settings.context_settings import ContextSettings
from cl.runtime.settings.project_settings import ProjectSettings
from cl.runtime.tasks.task import Task
from cl.runtime.tasks.task_key import TaskKey
from cl.runtime.tasks.task_queue import TaskQueue
from cl.runtime.tasks.task_queue_key import TaskQueueKey
from cl.runtime.tasks.task_status_enum import TaskStatusEnum

CELERY_MAX_WORKERS = 4

CELERY_RUN_COMMAND_QUEUE: Final[str] = "run_command"
CELERY_MAX_RETRIES: Final[int] = 3
CELERY_TIME_LIMIT: Final[int] = 3600 * 2  # TODO: 2 hours (configure)

databases_dir = ProjectSettings.get_databases_dir()
context_id = ContextSettings.instance().context_id

# Get sqlite file name of celery broker based on database id in settings
celery_file = os.path.join(databases_dir, f"{context_id}.celery.sqlite")

celery_sqlite_uri = f"sqlalchemy+sqlite:///{celery_file}"

celery_app = Celery(
    "worker",
    broker=celery_sqlite_uri,
    broker_connection_retry_on_startup=True,
)

celery_app.conf.task_track_started = True

context_serializer = DictSerializer()
"""Serializer for the context parameter of 'execute_task' method."""


@celery_app.task(max_retries=0)  # Do not retry failed tasks
def execute_task(
    task_id: str,
    context_data: TDataDict,
) -> None:
    """Invoke 'run_task' method of the specified task."""

    # Set is_deserialized flag in context data, will be used to skip some of the initialization code
    context_data["is_deserialized"] = True

    # Deserialize context from 'context_data' parameter to run with the same settings as the caller context
    with context_serializer.deserialize_data(context_data) as context:

        # Load and run the task
        task_key = TaskKey(task_id=task_id)
        task = context.load_one(Task, task_key)
        task.run_task()


def celery_start_queue_callable(*, log_dir: str) -> None:
    """
    Callable for starting the celery queue process.

    Args:
        log_dir: Directory where Celery console log file will be written
    """

    # Redirect console output from celery to a log file
    # TODO: Use an additional Logger handler instead
    log_file_path = os.path.join(log_dir, "celery_queue.log")
    # with open(log_file_path, "w") as log_file:
    #    os.dup2(log_file.fileno(), 1)  # Redirect stdout (file descriptor 1)
    #    os.dup2(log_file.fileno(), 2)  # Redirect stderr (file descriptor 2)

    celery_app.worker_main(
        argv=[
            "-A",
            "cl.runtime.tasks.celery.celery_queue",
            "worker",
            "--loglevel=info",
            f"--autoscale={CELERY_MAX_WORKERS},1",
            f"--pool=solo",  # One concurrent task per worker, do not switch to prefork (not supported on Windows)
            f"--concurrency=1",  # Use only for prefork, one concurrent task per worker (similar to solo)
        ],
    )


def celery_delete_existing_tasks() -> None:
    """Delete the existing Celery tasks (will exit when the current process exits)."""

    # Remove sqlite file of celery broker if exists
    if os.path.exists(celery_file):
        os.remove(celery_file)


def celery_start_queue(*, log_dir: str) -> None:
    """
    Start Celery workers (will exit when the current process exits).

    Args:
        log_dir: Directory where Celery console log file will be written
    """
    worker_process = multiprocessing.Process(
        target=celery_start_queue_callable, daemon=True, kwargs={"log_dir": log_dir}
    )
    worker_process.start()


@dataclass(slots=True, kw_only=True)
class CeleryQueue(TaskQueue):
    """Execute tasks using Celery."""

    # max_workers: int = missing()  # TODO: Implement support for max_workers
    """The maximum number of processes running concurrently."""

    # TODO: @abstractmethod
    def run_start_queue(self) -> None:
        """Start queue workers."""

    # TODO: @abstractmethod
    def run_stop_queue(self) -> None:
        """Cancel all active runs and stop queue workers."""

    def submit_task(self, task: TaskKey):
        # Get and serialize current context
        context = Context.current()
        context_data = context_serializer.serialize_data(context)

        # Pass parameters to the Celery task signature
        execute_task_signature = execute_task.s(
            task.task_id,
            context_data,
        )

        # Submit task to Celery with completed and error links
        execute_task_signature.apply_async(
            retry=False,  # Do not retry in case the task fails
            ignore_result=True,  # TODO: Do not publish to the Celery result backend
        )
