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
from cl.runtime.records.dataclasses.dataclass_mixin import DataclassMixin
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.decorators.handler_decorator import handler
from logging import getLogger
from stubs.cl.runtime.records.enum.stub_int_enum import StubIntEnum
from typing import Tuple, Any
from typing import Type

_logger = getLogger(__name__)


def print_method_info():  # TODO: Move into DebugUtil(s)
    """Print information about the caller method."""
    frame = inspect.currentframe()
    outer_frame = frame.f_back
    method_name = outer_frame.f_code.co_name
    args, _, _, values = inspect.getargvalues(outer_frame)

    params_output = ",".join(f"{arg}={values[arg]}" for arg in args)
    print(f"Called {method_name}({params_output})")


StubHandlerMethodsKey = Tuple[Type["StubHandlerMethods"], str]


class StubHandlerMethods(DataclassMixin):
    """Stub record base class."""

    stub_id: str = datafield(default="abc")
    """Stub identifier."""

    def get_key(self) -> StubHandlerMethodsKey:
        return type(self), self.stub_id

    @handler
    def instance_handler_1a(self) -> None:
        """Stub handler."""
        print_method_info()

    @handler()
    def instance_handler_1b(self) -> None:
        """Stub handler."""
        print_method_info()

    @handler
    def instance_handler_2a(self, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @handler()
    def instance_handler_2b(self, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @handler
    def instance_handler_3a(self, *, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @handler()
    def instance_handler_3b(self, *, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @classmethod
    @handler
    def class_handler_1a(cls) -> None:
        """Stub handler."""
        print_method_info()

    @classmethod
    @handler()
    def class_handler_1b(cls) -> None:
        """Stub handler."""
        print_method_info()

    @classmethod
    @handler
    def class_handler_2a(cls, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @classmethod
    @handler()
    def class_handler_2b(cls, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @classmethod
    @handler
    def class_handler_3a(cls, *, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @classmethod
    @handler()
    def class_handler_3b(cls, *, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @staticmethod
    @handler
    def static_handler_1a() -> None:
        """Stub handler."""
        print_method_info()

    @staticmethod
    @handler()
    def static_handler_1b() -> None:
        """Stub handler."""
        print_method_info()

    @staticmethod
    @handler
    def static_handler_2a(param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @staticmethod
    @handler()
    def static_handler_2b(param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @staticmethod
    @handler
    def static_handler_3a(*, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    @staticmethod
    @handler()
    def static_handler_3b(*, param1: str, param2: str = None) -> None:
        """Stub handler."""
        print_method_info()

    def handler_with_args(
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

    def handler_with_args(self, arg_1: str, arg_2: str) -> str:
        """Stub method."""
        return arg_1 + arg_2

    def handler_with_args_and_optional(self, arg_1: str, arg_2: str, arg_3: str = None) -> str:
        """Stub method."""
        return arg_1 + arg_2

    def handler_with_reserved_param_name(self, from_: dt.date = None) -> dt.date:
        """Stub method."""
        return from_

    def handler_with_error(self):
        """Stub method."""
        raise RuntimeError("Error in handler.")
