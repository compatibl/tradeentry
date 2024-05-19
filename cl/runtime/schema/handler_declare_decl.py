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

from typing import List, Optional

from cl.runtime.schema.handler_param_decl import HandlerParamDecl
from cl.runtime.schema.handler_type import HandlerType
from cl.runtime.schema.handler_variable_decl import HandlerVariableDecl
from dataclasses import dataclass
from cl.runtime.records.dataclasses.dataclass_mixin import datafield


@dataclass(slots=True)
class HandlerDeclareDecl:
    """Handler declaration data."""

    name: str = datafield()
    """Handler name."""

    label: str | None = datafield()
    """Handler label."""

    comment: str | None = datafield()
    """Handler comment."""

    type_: HandlerType = datafield(name='Type')
    """Handler type."""

    params: Optional[List[HandlerParamDecl]] = datafield()
    """Handler parameters."""

    return_: Optional[HandlerVariableDecl] = datafield(name='Return')
    """Handler return value."""

    static: Optional[bool] = datafield()
    """If set as true, handler will be static, elsewise non-static."""

    hidden: Optional[bool] = datafield()
    """If flag is set, handler will be hidden in UI in user mode."""
