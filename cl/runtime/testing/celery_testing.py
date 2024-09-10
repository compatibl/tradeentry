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
from cl.runtime.tasks.celery.celery_queue import celery_start_workers_process


@pytest.fixture(scope='session')
def celery_start_test_workers():
    print("Starting test celery workers.")
    celery_start_workers_process()   # TODO: Make test celery a separate queue
    yield
    # TODO: Do we need to explicitly shut down
    print("\nStopping test celery workers.")
