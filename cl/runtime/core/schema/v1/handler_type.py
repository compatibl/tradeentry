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

from enum import IntEnum

from cl.runtime.core.storage.class_label import class_label


@class_label('(Analyst) Handler Type')
class HandlerType(IntEnum):
    """Handler type enumeration."""

    Job = 0
    """
    Job handler. Return type is allowed but will be discarded in case of invocation from the client. Input params are
    allowed
    """

    Process = 1
    """Process handler. Return type is not allowed. Input params are allowed"""

    Viewer = 2
    """Viewer handler. Return type is allowed. Input params are not allowed."""

    Editor = 3
    """Viewer Editor. Return type is allowed. Input params are not allowed."""
