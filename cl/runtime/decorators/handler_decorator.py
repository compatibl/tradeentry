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


def handler_impl(method, *, label=None):
    """Decorator to mark methods that perform user action."""
    method._is_handler = True
    return method


def handler(method=None, *, label=None):
    """Decorator to mark methods that perform user action."""

    # The first parameter is the method when decorator does not have parentheses and None when it does
    if method is None:
        return handler_impl
    else:
        return handler_impl(method, label=label)
