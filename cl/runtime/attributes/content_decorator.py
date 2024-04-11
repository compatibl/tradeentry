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


import inspect
from cl.runtime.attributes.handler_decorator import handler
from itertools import islice
from typing import Any
from typing import Callable


def content(method: Callable[..., Any]):
    """
    Decorator for identifying content methods.
    A content method must not take any parameters.
    """

    if inspect.isfunction(method) or inspect.ismethod(method):
        # Checking for parameters
        method_params = dict(inspect.signature(method).parameters)
        starts_from = 1 if "self" in method_params.keys() else 0
        params = list(islice(method_params.values(), starts_from, None))
        if params:
            raise Exception("The function decorated by the 'content' decorator should not have any input parameters.")

        expected_return_type = inspect.signature(method).return_annotation
        if expected_return_type is not str:
            raise TypeError(
                "The function decorated by the 'content' decorator should return string.",
            )

        method = handler(language=language)(method)

        method._cl_content = True
        return method
