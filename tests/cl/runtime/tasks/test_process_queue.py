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
from cl.runtime.tasks.process_queue import ProcessQueue
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.runtime.tasks.stub_task import StubTask


def test_process_queue():
    """Test ProcessQueue class."""

    with TestingContext() as context:

        guard = RegressionGuard()

        # Create queue
        queue = ProcessQueue(queue_id="test_process_queue")
        queue_key = queue.get_key()

        # Create and save tasks
        task_count = 2
        tasks = [StubTask(label=f"{i}", queue=queue_key) for i in range(task_count)]
        context.save_many(tasks)

        # Start queue
        queue.start_queue()

        # Stop queue
        # TODO: Stop queue

        guard.verify()


if __name__ == "__main__":
    pytest.main([__file__])
