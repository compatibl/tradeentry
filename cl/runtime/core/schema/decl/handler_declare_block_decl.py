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
from typing import List

from cl.runtime.core.schema.decl.handler_declare_decl import HandlerDeclareDecl
from cl.runtime.core.storage.class_data import ClassData, class_field
from cl.runtime.core.storage.class_label import class_label


@class_label('Handler Declare Block Declaration')
@dataclass
class HandlerDeclareBlockDecl(ClassData):
    """Handler declaration block in type declaration."""

    handlers: List[HandlerDeclareDecl] = class_field()
    """Handler declaration data."""
