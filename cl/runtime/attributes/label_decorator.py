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
from cl.runtime.storage.data_mixin import DataMixin
from enum import IntEnum
from typing import Protocol


def label(label: str):
    """Decorator to set label for data class or enum.
    If specified, will be used in the user interface instead of the name.
    This field has no effect on the API and affects only the user interface.
    """

    def wrap(obj):
        if inspect.isclass(obj):
            if (DataMixin not in obj.__mro__) and (IntEnum not in obj.__mro__) and (Protocol not in obj.__mro__):
                raise Exception('@label should be applied on Data derived class, IntEnum or Protocol')

            obj._label = label
            return obj
        elif inspect.isfunction(obj) or inspect.ismethod(obj):
            obj._label = label
            return obj
        else:
            raise Exception('@label should be applied on class or method')

    return wrap
