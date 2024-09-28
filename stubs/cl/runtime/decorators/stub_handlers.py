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

import datetime as dt
import inspect
from dataclasses import dataclass
from logging import getLogger
from typing import Any
from cl.runtime.context.context import Context
from cl.runtime.decorators.handler_decorator import handler
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.record_mixin import RecordMixin
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.decorators.stub_handlers_key import StubHandlersKey
from stubs.cl.runtime.records.enum.stub_int_enum import StubIntEnum

_logger = getLogger(__name__)


def log_method_info(name: str):  # TODO: Move into testing directory
    """Print information about the caller method."""

    # Get logger from the current context
    context = Context.current()
    logger = context.get_logger(name)

    # Record method information from stack frame
    current_frame = inspect.currentframe()
    outer_frame = current_frame.f_back
    method_name = outer_frame.f_code.co_name
    args, _, _, values = inspect.getargvalues(outer_frame)

    # Explicitly delete the frames to avoid circular references
    del outer_frame
    del current_frame

    # Log information
    params_output = ",".join(f"{arg}={values[arg]}" for arg in args)
    logger.info(f"Called {method_name}({params_output})")


@dataclass(slots=True, kw_only=True)
class StubHandlers(StubHandlersKey, RecordMixin[StubHandlersKey]):
    """Stub record base class."""

    def get_key(self) -> StubHandlersKey:
        return StubHandlersKey(stub_id=self.stub_id)

    @handler
    def run_instance_method_1a(self) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @handler()
    def run_instance_method_1b(self) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @handler
    def run_instance_method_2a(self, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @handler()
    def run_instance_method_2b(self, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @handler
    def run_instance_method_3a(self, *, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @handler()
    def run_instance_method_3b(self, *, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @classmethod
    @handler
    def run_class_method_1a(cls) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @classmethod
    @handler()
    def run_class_method_1b(cls) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @classmethod
    @handler
    def run_class_method_2a(cls, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @classmethod
    @handler()
    def run_class_method_2b(cls, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @classmethod
    @handler
    def run_class_method_3a(cls, *, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @classmethod
    @handler()
    def run_class_method_3b(cls, *, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @staticmethod
    @handler
    def run_static_method_1a() -> None:
        """Stub handler."""
        log_method_info(__name__)

    @staticmethod
    @handler()
    def run_static_method_1b() -> None:
        """Stub handler."""
        log_method_info(__name__)

    @staticmethod
    @handler
    def run_static_method_2a(param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @staticmethod
    @handler()
    def run_static_method_2b(param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @staticmethod
    @handler
    def run_static_method_3a(*, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @staticmethod
    @handler()
    def run_static_method_3b(*, param1: str, param2: str = None) -> None:
        """Stub handler."""
        log_method_info(__name__)

    @handler
    def run_with_args(
        self,
        int_arg: int,
        datetime_arg: dt.datetime,
        enum_arg: StubIntEnum,
        data_arg: Any,
    ) -> None:
        _logger.info(
            f"handler_with_arguments(int_arg={int_arg} datetime_arg={datetime_arg}"
            f"enum_arg={enum_arg} data_arg={data_arg})"
        )

    @handler
    def run_with_two_args(self, arg_1: str, arg_2: str) -> str:
        """Stub method."""
        return arg_1 + arg_2

    @handler
    def run_with_args_and_optional(self, arg_1: str, arg_2: str, arg_3: str = None) -> str:
        """Stub method."""
        return arg_1 + arg_2

    @handler
    def run_with_reserved_param_name(self, from_: dt.date = None) -> dt.date:
        """Stub method."""
        return from_

    @handler
    def run_with_error(self):
        """Stub method."""
        raise RuntimeError("Error in handler.")

    @handler
    def run_save_to_db(self):
        log_method_info(__name__)
        data_source = Context.current().data_source
        stub = StubDataclassRecord(id="saved_from_handler")
        data_source.save_one(stub)
