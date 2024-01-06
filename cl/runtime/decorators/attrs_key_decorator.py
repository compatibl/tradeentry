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

import attrs
from typing_extensions import dataclass_transform
from cl.runtime.decorators.attrs_data_decorator import attrs_data_impl


@dataclass_transform()
def attrs_key_impl(cls, *, label=None):
    """Performs the actual wrapping irrespective of call syntax with or without parentheses."""

    cls = attrs_data_impl(cls)

    get_table_method = getattr(cls, "get_table", None)
    if get_table_method is not None and getattr(get_table_method, "_implemented", False):
        # Use the method from parent if marked by _implemented, which will not be present
        # if the method is declared in parent class without implementation. Reassignment
        # here accelerates the code by preventing lookup at each level of inheritance chain.
        cls.get_table = get_table_method
    else:
        # Implement using module and class name here and mark by _implemented
        # TODO: Use package alias if specified in settings
        def get_table(self):
            return f"{cls.__module__}.{cls.__name__}"  # TODO: Remove trailing 'Key' if present

        cls.get_table = get_table
        cls.get_table._implemented = True

    get_key_method = getattr(cls, "get_key", None)
    if get_key_method is not None and getattr(get_key_method, "_implemented", False):
        # Use the method from parent if marked by _implemented, which will not be present
        # if the method is declared in parent class without implementation. Reassignment
        # here accelerates the code by preventing lookup at each level of inheritance chain.
        cls.get_key = get_key_method
    else:
        # Implement using module and class name here and mark by _implemented
        # TODO: Use package alias if specified in settings
        field_names = {f.name: f for f in attrs.fields(cls)}

        def get_key(self):
            # TODO: Use type-aware method for conversion to string
            # TODO: Review performance impact
            field_values = [str(getattr(self, field_name, None)) for field_name in field_names]
            return ';'.join(field_values)

        cls.get_key = get_key
        cls.get_key._implemented = True

    to_key_method = getattr(cls, "to_key", None)
    if to_key_method is not None and getattr(to_key_method, "_implemented", False):
        # Use the method from parent if marked by _implemented, which will not be present
        # if the method is declared in parent class without implementation. Reassignment
        # here accelerates the code by preventing lookup at each level of inheritance chain.
        cls.to_key = to_key_method
    else:
        # Implement using module and class name here and mark by _implemented
        # TODO: Use package alias if specified in settings
        field_names = {f.name: f for f in attrs.fields(cls)}

        def to_key(self):
            key = cls()
            for field_name in field_names.values():  # TODO: Review performance impact
                value = getattr(self, field_name, None)
                setattr(key, field_name, value)
            return key

        cls.to_key = to_key
        cls.to_key._implemented = True

    return cls


@dataclass_transform()
def attrs_key(cls=None, *, label=None):
    """Runtime decorator for key, record, and data classes."""

    # The value of cls type depends on whether parentheses follow the decorator.
    # It is the class when used as @attrs_key but None for @attrs_key().
    if cls is None:
        return attrs_key_impl
    else:
        return attrs_key_impl(cls, label=label)
