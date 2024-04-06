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

from cl.runtime.storage.key_mixin import KeyMixin
from functools import wraps
from inspect import Parameter
from inspect import isfunction
from inspect import ismethod
from inspect import signature
from itertools import islice
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Tuple


def handler(label: str = None):
    """
    Decorator for identifying class or static methods that are handlers.
    Handlers are methods that can be invoked through the user interface or CLI.

    A handler must return void and its parameters must be valid field types.
    """

    def wrap(method: Callable):
        if not isfunction(method) and not ismethod(method):
            raise Exception('@handler decorator can only be applied to a class or static method.')

        wrapped_method = method
        wrapped_method._handler = True
        if label is not None:
            wrapped_method._label = label
        return wrapped_method

    return wrap


def _parse_params(method: Callable, method_params: Iterable[Parameter], args: Tuple, kwargs: Dict):
    """Get parameters other than self (use for instance and static methods)."""

    # Get method parameters
    params: Dict[str, Any] = dict()
    args_count = len(args)

    for i, param in enumerate(method_params):
        # get param value
        if i < args_count:
            param_value = args[i]
        elif param.name in kwargs:
            param_value = kwargs[param.name]
        elif param.default != Parameter.empty:
            param_value = param.default
        else:
            raise Exception(f'Wrong arguments count for {method.__qualname__} handler.')

        params[param.name] = param_value

    return params


def _get_params(method: Callable, args: Tuple, kwargs: Dict, ignore_self_arg: bool = False) -> Tuple[KeyMixin, Dict]:
    """Get parameters including self (use for instance methods only)."""

    method_params = signature(method).parameters

    self_param: Optional[KeyMixin] = None
    params_values: Any = method_params.values()
    args_values = args

    # Get parameter self
    if 'self' in method_params.keys():
        if not ignore_self_arg:
            self_param = args[0]
            args_values = args[1:]
        params_values = islice(params_values, 1, None)

    return self_param, _parse_params(method, params_values, args_values, kwargs)
