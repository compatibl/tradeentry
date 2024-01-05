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


@dataclass_transform()
def attrs_data_impl(cls, *, label=None):
    """Performs the actual wrapping irrespective of call syntax with or without parentheses."""

    cls = attrs.define(cls)

    # Remove base fields
    fields = {f.name: f for f in attrs.fields(cls) if not f.inherited}

    def to_dict(self):
        return attrs.asdict(self)
    cls.to_dict = to_dict

    def from_dict(self, data):
        raise NotImplementedError()  # TODO: currently a stub

    return cls


@dataclass_transform()
def attrs_data(cls=None, *, label=None):
    """Runtime decorator for key, record, and data classes."""

    # The value of cls type depends on whether parentheses follow the decorator.
    # It is the class when used as @attrs_data but None for @attrs_data().
    if cls is None:
        return attrs_data_impl
    else:
        return attrs_data_impl(cls, label=label)
