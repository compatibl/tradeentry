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
from typing import Any, List, Optional, Tuple, Type

from cl.runtime.attributes import ImplementLanguage, MethodTrait
from cl.runtime.storage.class_info import ClassInfo
from cl.runtime.storage.data_mixin import DataMixin
from cl.runtime.storage.attrs import data_class, data_field


@data_class
class MethodArgumentInfo(DataMixin):
    """Method argument information class."""

    name: Optional[str] = data_field()
    """Argument name."""

    type: Optional[Type] = data_field()
    """Argument type."""

    default: Optional[Any] = data_field()
    """Argument default value."""

    optional: Optional[bool] = data_field()
    """Argument is optional flag."""


@data_class
class MethodInfo(DataMixin):
    """Method information class."""

    method_name: Optional[str] = data_field()
    """Method name."""

    label: Optional[str] = data_field()
    """Method label added by label decorator."""

    is_cl_viewer: Optional[bool] = data_field()
    """Method is viewer flag. True if method is decorated by viewer."""

    is_cl_process: Optional[bool] = data_field()
    """Method is process flag. True if method is decorated by process."""

    is_cl_handler: Optional[bool] = data_field()
    """Method is handler flag. True if method is decorated by handler."""

    is_cl_content: Optional[bool] = data_field()
    """Method is content flag. True if method is decorated by content."""

    is_abstract: Optional[bool] = data_field()
    """Method is abstract flag."""

    is_static: Optional[bool] = data_field()
    """Method is static flag."""

    hidden: Optional[bool] = data_field()
    """Method trait hidden. Check MethodTrait enum docs."""

    interactive_input: Optional[bool] = data_field()
    """Method trait interactive input. Check MethodTrait enum docs."""

    is_async: Optional[bool] = data_field()
    """Method trait is async. Check MethodTrait enum docs."""

    handler_traits: Optional[Tuple[MethodTrait]] = data_field()
    """Handler traits added by handler decorator."""

    handler_language: Optional[ImplementLanguage] = data_field()
    """Handler language added by handler decorator."""

    docstring: Optional[str] = data_field()
    """Method docstring."""

    return_type: Optional[type] = data_field()
    """Method return type."""

    arguments: Optional[List[MethodArgumentInfo]] = data_field()
    """List of method arguments info."""

    def __init__(self, type_: Type, method_name: str):
        """Extract type method information."""

        self.method_name = method_name
        method = getattr(type_, method_name, None)

        if method is None:
            raise ValueError(f'Type {type_.__name__} does not have method {method_name}')

        # added by handler decorator
        self.label = method.__dict__.get('_label', None)

        # added by viewer decorator
        self.is_cl_viewer = hasattr(method, '_cl_viewer')

        # added by process decorator
        self.is_cl_process = hasattr(method, '_cl_process')

        # added by handler decorator
        self.is_cl_handler = hasattr(method, '_cl_handler')

        self.is_cl_content = hasattr(method, '_cl_content')

        self.is_abstract = getattr(method, '__isabstractmethod__', False)
        self.is_static = isinstance(inspect.getattr_static(type_, method_name), staticmethod)

        self.hidden = False
        self.interactive_input = False
        self.is_async = False

        # check _cl_handler_traits added by handler decorator
        self.handler_traits = None
        if '_cl_handler_traits' in method.__dict__:
            handler_traits: Tuple[MethodTrait] = method._cl_handler_traits
            self.handler_traits = handler_traits
            for item in handler_traits:
                if item == MethodTrait.Hidden:
                    self.hidden = True
                elif item == MethodTrait.InteractiveInput:
                    self.interactive_input = True
                elif item == MethodTrait.IsAsync:
                    self.is_async = True

        self.handler_language = None
        if self.is_cl_handler or self.is_cl_content and method._cl_handler_language is not None:
            self.handler_language = method._cl_handler_language

        self.docstring = getattr(method, '__doc__')
        method_hints = ClassInfo.get_type_hints(method)
        self.return_type = method_hints.get('return', inspect.Signature.empty)

        self.arguments = []
        method_arguments = inspect.signature(method)

        for i, parameter in enumerate(method_arguments.parameters.values()):  # type: int, inspect.Parameter
            argument_info = MethodArgumentInfo(
                name=parameter.name,
                type=method_hints.get(parameter.name, inspect.Parameter.empty),
                default=parameter.default,
                optional=parameter.default is not inspect.Parameter.empty and parameter.default is None,
            )
            self.arguments.append(argument_info)
