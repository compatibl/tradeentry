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

import re
import uuid
from dataclasses import dataclass
from typing import Dict, Any, Type, Callable

from inflection import underscore
from cl.runtime.context.context import current_or_default_data_source
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.protocols import KeyProtocol, RecordProtocol
from cl.runtime.tasks.v1.task_observer import TaskObserver
from cl.runtime.tasks.v1.task_run import TaskRunV1
from cl.runtime.tasks.v1.task_status import TaskStatus


@dataclass
class TaskRunner:
    """Class to run task on record or class with specified args."""

    # TODO (Roman): support run task on live object
    record_key: KeyProtocol | None = missing()
    """Key of record for which task will be executed."""

    record_type: Type[RecordProtocol] | None = missing()
    """Record type for which task will be executed."""

    handler: str | None = missing()
    """Name of handler which will be executed in task."""

    args: Dict[str, Any] | None = missing()
    """Handler args."""

    def submit(self) -> TaskObserver:
        """
        Submit task and return TaskObserver.

        Submitted task has specific TaskRun record in db with status info. Status will change according to task
        completion: if task completed successfully TaskRun record will have status "Completed" and some result object,
        if failed - status "Failed" and error message in result.
        """

        if self.record_key is None and self.record_type is None:
            raise RuntimeError("Can not submit task without record key and record type.")

        # create unique run_id
        run_id = uuid.uuid1()

        # save TaskRun with status "Submitted"
        data_source = current_or_default_data_source()
        data_source.save_one(TaskRunV1(id=run_id, status=TaskStatus.Submitted, key=self.record_key))

        # run instance or static handler as task
        if self.record_key is not None:
            self._run_instance_task(run_id)
        else:
            self._run_static_task(run_id)

        return TaskObserver(task_run_id=run_id)

    def _run_instance_task(self, run_id: uuid.UUID) -> None:

        # load record from db
        data_source = current_or_default_data_source()
        record = data_source.load_one(self.record_key)

        # run callable as task
        callable_ = getattr(record, self._get_method_name())
        self._run_callable_as_task(run_id, callable_, self.args)

    def _run_static_task(self, run_id: uuid.UUID) -> None:
        # run callable as task
        # TODO (Roman): add class as first arg for classmethods
        callable_ = getattr(self.record_type, self._get_method_name())
        self._run_callable_as_task(run_id, callable_, self.args)

    def _get_method_name(self) -> str:
        prev_name = underscore(self.handler)

        # add underscore before numbers
        return re.sub(r"([0-9]+)", r"_\1", prev_name)

    @staticmethod
    def _run_callable_as_task(run_id: uuid.UUID, callable_: Callable, args: Dict[str, Any] | None) -> None:

        # set empty args
        args = args if args is not None else {}

        # TODO (Roman): support async handlers
        data_source = current_or_default_data_source()
        try:
            # run callable
            result = callable_(**args)
        except Exception as exc:
            # update TaskRun with status "Failed" and error message in result
            data_source.save_one(TaskRunV1(id=run_id, status=TaskStatus.Failed, result=f"{type(exc)}: {exc}."))
        else:
            # update TaskRun with status "Completed" and callable result
            data_source.save_one(TaskRunV1(id=run_id, status=TaskStatus.Completed, result=result))
