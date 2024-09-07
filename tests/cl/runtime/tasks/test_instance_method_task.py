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
from cl.runtime.tasks.instance_method_task import InstanceMethodTask
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers


def test_create():
    """Test 'test_create' method."""

    with Context() as context:
        records = [StubHandlers(stub_id="abc")]
        context.data_source.save_many(records)

        sample_handler_tuples = (
            [(x.get_key(), StubHandlers.instance_handler_1a) for x in records]
            + [(x, StubHandlers.class_handler_1a) for x in records]
            + [(x, x.instance_handler_1a) for x in records]
        )

        for sample_handler_tuple in sample_handler_tuples:
            record_or_key = sample_handler_tuple[0]
            method_callable = sample_handler_tuple[1]
            task = InstanceMethodTask.create(
                task_id="abc",
                method_callable=method_callable,
                record_or_key=record_or_key,
            )
            task.execute()


if __name__ == "__main__":
    pytest.main([__file__])
