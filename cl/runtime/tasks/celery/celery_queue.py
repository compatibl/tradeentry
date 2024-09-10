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
from typing import Final, List, Optional
from celery import Celery

CELERY_MAX_WORKERS = 4

CELERY_RUN_COMMAND_QUEUE: Final[str] = 'run_command'
CELERY_MAX_RETRIES: Final[int] = 3
CELERY_TIME_LIMIT: Final[int] = 3600 * 2

celery_app = Celery(
    "worker",
    broker="mongodb://localhost:27017/celery",
    backend="mongodb://localhost:27017/celery",
    broker_connection_retry_on_startup=True,
    # include=['cl.runtime.tasks.celery.celery_app_2']
)

celery_app.conf.task_track_started = True


@celery_app.task
def celery_callable():
    return 10


def celery_start_workers(worker_name: Optional[str] = None, queue_names: Optional[List[str]] = None) -> None:

    # Celery doesn't support Windows
    pool = "solo" if platform.system() != 'Linux' else "prefork"

    celery_app.worker_main(
        argv=[
            '-A',
            'cl.runtime.tasks.celery.celery_queue',
            'worker',
            '--loglevel=info',
            f'--autoscale={CELERY_MAX_WORKERS},1',
            f'--pool={pool}',
        ],
    )


def celery_start_workers_process(worker_name: Optional[str] = None, queue_names: Optional[List[str]] = None) -> None:

    # Start Celery workers (will exit when the current process exits)
    worker_process = multiprocessing.Process(target=celery_start_workers, daemon=True)
    worker_process.start()
