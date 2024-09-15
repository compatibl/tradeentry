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
import os
from cl.runtime.tasks.celery.celery_queue import celery_delete_existing_tasks
from cl.runtime.tasks.celery.celery_queue import celery_start_queue


@pytest.fixture(scope="module")
def local_dir_fixture(request):
    """Pytest module fixture to make test module directory the local directory during test execution."""

    # Change test working directory to the directory of test source
    # so output files are placed next to the test module
    os.chdir(request.fspath.dirname)

    # Back to the test
    yield

    # Change directory back before exiting the text
    os.chdir(request.config.invocation_dir)


@pytest.fixture(scope="session")
def celery_test_queue_fixture():
    """Pytest session fixture to start Celery test queue for test execution."""
    print("Starting celery workers, will delete the existing tasks.")
    celery_delete_existing_tasks()
    celery_start_queue()  # TODO: Make test celery a separate queue
    yield
    celery_delete_existing_tasks()
    print("Stopping celery workers and cleaning up tasks.")
