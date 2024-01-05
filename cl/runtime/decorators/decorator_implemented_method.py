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

from typing import Callable, ClassVar, Any


def decorator_implemented_method_impl(method: Callable[[Any], str]) -> Callable[[Any], str]:
    """
    Indicates that the implementation raises an exception, making this effectively an abstract method.
    Use when the implementation is by a decorator rather than in code, causing static type checkers
    to report an error for @abstractmethod.

    This decorator performs the actual wrapping irrespective of call syntax with or without parentheses.
    In code, @decorator_implemented_method should be used instead.
    """
    method._decorator_implemented_method = True
    return method


def decorator_implemented_method(method: Callable[[Any], str] = None) -> Callable[[Callable[[Any], str]], Callable[[Any], str]]:
    """
    Indicates that the implementation raises an exception, making this effectively an abstract method.
    Use when the implementation is by a decorator rather than in code, causing static type checkers
    to report an error for @abstractmethod.
    """

    # The value of method type depends on whether parentheses follow the decorator.
    # It is the class when used as @decorator_implemented_method but None for @decorator_implemented_method().
    if method is None:
        return decorator_implemented_method_impl
    else:
        return decorator_implemented_method_impl(method)

