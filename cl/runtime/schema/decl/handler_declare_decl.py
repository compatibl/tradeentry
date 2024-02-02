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

from cl.runtime.storage.attrs import attrs_field, attrs_class
from typing import List, Optional

from cl.runtime.schema.decl.handler_param_decl import HandlerParamDecl
from cl.runtime.schema.decl.handler_type import HandlerType
from cl.runtime.schema.decl.handler_variable_decl import HandlerVariableDecl
from cl.runtime.storage.data import Data


@attrs_class
class HandlerDeclareDecl(Data):
    """Handler declaration data."""

    name: str = attrs_field()
    """Handler name."""

    label: Optional[str] = attrs_field()
    """Handler label."""

    comment: Optional[str] = attrs_field()
    """Handler comment."""

    type_: HandlerType = attrs_field(name='Type')
    """Handler type."""

    params: Optional[List[HandlerParamDecl]] = attrs_field()
    """Handler parameters."""

    return_: Optional[HandlerVariableDecl] = attrs_field(name='Return')
    """Handler return value."""

    static: Optional[bool] = attrs_field()
    """If set as true, handler will be static, otherwise non-static."""

    hidden: Optional[bool] = attrs_field()
    """If flag is set, handler will be hidden in UI in user mode."""

    interactive_input: Optional[bool] = attrs_field()
    """Interactive Input"""

    category: Optional[str] = attrs_field()
    """Category."""

    is_async: Optional[bool] = attrs_field()
    """Use the flag to specify that a handler is asynchronous."""
