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

import attrs
from typing import Dict
from typing_extensions import dataclass_transform
from cl.runtime.storage.record_util import RecordUtil
from cl.runtime.storage.data import Data
from cl.runtime.storage.key import Key


@dataclass_transform()
def attrs_key_impl(cls, *, label=None):
    """Performs the actual wrapping irrespective of call syntax with or without parentheses."""

    cls = attrs.define(cls)

    if not issubclass(cls, Data):
        raise TypeError('Expected Data derived type.')

    if not attrs.has(cls):
        raise TypeError('Expected attrs type.')

    # Remove base fields
    fields = {f.name: f for f in attrs.fields(cls) if not f.inherited}

    # Add __str__ and to_key realizations for key type
    if Key in cls.__bases__:
        _add_key_methods(cls, fields)

    # Add label if specified
    if label is not None:
        cls._label = label

    def init(self):
        pass
    cls.init = init

    def to_dict(self):
        return attrs.asdict(self)
    cls.to_dict = to_dict

    def from_dict(self, data):
        raise NotImplementedError()  # TODO: currently a stub

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
            return cls.__name__
        cls.get_table = get_table
        cls.get_table._implemented = True

    def from_dict(self, data):
        raise NotImplementedError()  # TODO: currently a stub

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


def _add_key_methods(cls, fields: Dict[str, attrs.Attribute]):
    """Add __str__ and to_key realizations for key type."""

    data_fields = attrs.fields(Data)
    key_attributes = [x for x in fields.values() if x not in data_fields]

    def to_key(self):
        key = cls()
        for field in fields.values():
            field_name = field.name
            value = getattr(self, field_name, None)
            setattr(key, field_name, value)
        return key

    cls.to_key = to_key
