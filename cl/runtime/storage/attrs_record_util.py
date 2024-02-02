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
from cl.runtime.storage.attrs_key_util import attrs_key
from cl.runtime.storage.attrs_field_util import attrs_field


@dataclass_transform()
def attrs_record_impl(cls, *, init=True, label=None):
    """Performs the actual wrapping irrespective of call syntax with or without parentheses."""

    cls = attrs.define(cls, init=init)

    # Add label if specified
    if label is not None:
        cls._label = label

    init_method = getattr(cls, "init", None)
    if init_method is not None and getattr(init_method, "_implemented", False):
        # Use the method from parent if marked by _implemented, which will not be present
        # if the method is declared in parent class without implementation. Reassignment
        # here accelerates the code by preventing lookup at each level of inheritance chain.
        cls.init = init_method
    else:
        # Implement here and mark by _implemented
        def init(self):
            pass  # TODO: Implement hierarchical calls to parents but only when init has body
        cls.init = init
        cls.init._implemented = True

    return cls


@dataclass_transform()
def attrs_record(cls=None, *, init=True, label=None):
    """Runtime decorator for key, record, and data classes."""

    # The value of cls type depends on whether parentheses follow the decorator.
    # It is the class when used as @attrs_record but None for @attrs_record().
    if cls is None:
        return attrs_record_impl
    else:
        return attrs_record_impl(cls, init=init, label=label)
