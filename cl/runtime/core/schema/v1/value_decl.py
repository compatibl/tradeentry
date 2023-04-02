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

from dataclasses import dataclass

from cl.runtime.core.storage.class_label import class_label
from cl.runtime.core.schema.v1.atomic_type import AtomicType
from cl.runtime.core.storage.class_data import ClassData, class_field


@class_label('Value Declaration')
@dataclass
class ValueDecl(ClassData):
    """Value or atomic element declaration."""

    type_: AtomicType = class_field(name='Type')
    """Value or atomic element type enumeration."""
