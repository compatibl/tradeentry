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


class HandlerType(IntEnum):  # Consider renaming to MethodType
    """Handler type enumeration."""

    Job = 0  # TODO: Consider renaming to Action or Handler if class is renamed to MethodType
    """
    Job handler is shown as a button
    
    - Return type is allowed and may trigger action in the client.
    - Input params are allowed.
    """

    Process = 1
    """Process handler. Return type is not allowed. Input params are allowed"""

    Viewer = 2
    """Viewer handler. Return type is allowed. Input params are not allowed."""

    Content = 4
    """Content handler. Return type is allowed. Input params are not allowed."""
