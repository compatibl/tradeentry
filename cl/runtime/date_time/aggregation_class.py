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

from typing import Callable

# TODO: Refactor to make the API similar to other utilities


def create_aggregation_method(interface_method: str, cls) -> Callable:
    """Create aggregation method for specified interface method."""

    def aggregation_method(value, target_type=None):
        if target_type is None:
            target_type = type(value)

        if target_type not in cls._utils_map:
            raise Exception(f'Type {target_type.__name__} has not util class.')

        util_class = cls._utils_map[target_type]

        if not hasattr(util_class, interface_method):
            raise Exception(f'Util class {util_class.__name__} has not method {interface_method}.')

        real_method = getattr(util_class, interface_method)

        return real_method(value)

    return aggregation_method


def aggregation_class(cls):
    """
    Class decorator for generating aggregation methods inside class.
    Decorated class should have fields _methods_map and _utils_map.
    For each of methods in the _methods_map will be created aggregation method.

    Aggregation method signature:
        def method_name(value, expected_type=None)

    If an expected_type is None, type will be determine as a type(value).

    Aggregation method has a next logic (code snippet):
        def concrete_method_aggregation(value, expected_type=None):
            if expected_type == type_1:
                return util_for_type_1.concrete_method(value)
            elif expected_type == type_2:
                return util_for_type_2.concrete_method(value)
            else:
                raise Exception()
    """
    if not hasattr(cls, '_methods_map'):
        raise Exception(f'Class {str(cls)} has not _methods_map.')

    if not hasattr(cls, '_utils_map'):
        raise Exception(f'Class {str(cls)} has not _utils_map.')

    for interface_method, new_aggregation_method in cls._methods_map.items():
        setattr(
            cls,
            new_aggregation_method,
            staticmethod(create_aggregation_method(interface_method, cls)),
        )

    return cls
