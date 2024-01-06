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


def viewer(*, label: str = None):
    """
    Decorator for identifying class or static methods that are viewers.
    Viewers are invoked to display information about the record.

    A viewer return type and its parameters must be valid field types.
    """

    def wrap(method):
        if not inspect.isfunction(method) and not inspect.ismethod(method):
            raise Exception('@viewer decorator can only be applied to a class or static method.')

        wrapped_method = method
        wrapped_method._handler = True
        if label is not None:
            wrapped_method._label = label
        return wrapped_method

    return wrap
