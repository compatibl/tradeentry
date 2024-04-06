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

from cl.runtime.attributes.implement_language import ImplementLanguage
from cl.runtime.attributes.method_trait import MethodTrait
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


def _parse_method_params(method: Callable, method_params: Iterable[Parameter], args: Tuple, kwargs: Dict):
    """
    Parse the parameters of a given method based on the provided arguments.

    Parameters:
    - method (Callable): The method to parse.
    - method_params (Iterable[Parameter]): The parameters of the method.
    - args (Tuple): The positional arguments passed to the method.
    - kwargs (Dict): The keyword arguments passed to the method.

    Returns:
    Dict[str, Any]: A dictionary containing parameter names as keys and corresponding values.

    Raises:
    Exception: If there is a mismatch in the number of arguments for the method.
    """
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


def _get_parameters(
    method: Callable, args: Tuple, kwargs: Dict, ignore_self_arg: bool = False
) -> Tuple[KeyMixin, Dict]:
    """
    Get the parameters of a method, excluding the 'self' parameter if present.

    Parameters:
    - method (Callable): The method to retrieve parameters from.
    - args (Tuple): The positional arguments passed to the method.
    - kwargs (Dict): The keyword arguments passed to the method.
    - ignore_self_arg (bool, optional): If True, ignores the 'self' parameter. Defaults to False.

    Returns:
    Tuple[Optional[Key], Dict]: A tuple containing the 'self' parameter (if present) and a dictionary of parsed parameters.
    """
    method_params = signature(method).parameters

    self_param: Optional[KeyMixin] = None
    params_values: Any = method_params.values()
    args_values = args

    # get self parameter
    if 'self' in method_params.keys():
        if not ignore_self_arg:
            self_param = args[0]
            args_values = args[1:]
        params_values = islice(params_values, 1, None)

    return self_param, _parse_method_params(method, params_values, args_values, kwargs)


def handler(
    *args: MethodTrait,
    language: ImplementLanguage = ImplementLanguage.Python,
    metadata: Optional[Dict] = None,
):
    """
    Decorator for identifying functions that are handlers.

    Handlers are functions of a Record that can be invoked
    through the user interface or CLI.

    A handler must return void and either take no
    parameters, or take parameters that are a combination
    of:

    * Atomic types
    * Classes derived from Data

    While passing Record types as handler parameters is not
    prohibited, best practice is to pass such parameters by
    specifying their key rather than their data.
    """
    if len(args) == 1:
        method = args[0]
        if isfunction(method) or ismethod(method):
            method._cl_handler = True
            method._cl_handler_language = ImplementLanguage.Python
            method._cl_handler_traits = tuple()
            return method

    def wrap(method: Callable):
        if not isfunction(method) and not ismethod(method):
            raise Exception('@handler decorator should be applied on method or function.')

        wrapped_method = method
        wrapped_method._cl_handler = True
        wrapped_method._cl_handler_language = language
        wrapped_method._cl_handler_traits = args
        return wrapped_method

    return wrap
