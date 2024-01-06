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

from abc import ABC
from typing import Optional
from cl.runtime import Context
from cl.runtime.data.key import Key


class Record(ABC):
    """
    Optional mixin class for database records.

    - Record classes may implement handlers and viewers
    - Handlers are functions that can be invoked from the UI
    - Viewers are functions whose return value is displayed in the UI
    - Handlers and viewers may be either instance or class methods, and may have parameters

    The use of this class is optional. The code must not rely on inheritance from this class, but only on the
    presence of its methods. These methods may be implemented without using any specific base or mixin class.

    The methods that lack implementation must be overridden by a derived class in code or using a decorator.
    They are not made abstract to avoid errors from static type checkers in the latter case.
    """

    context: Optional[Context]
    """
    Context provides platform-independent APIs for:

    - Databases and distributed cache
    - Logging and error reporting
    - Local or remote handler execution
    - Progress reporting
    - Virtualized filesystem
    """

    def init(self) -> None:
        """Validate dataclass attributes and use them to initialize object state."""

        # NoOp by default, derived classes will override when required
        pass
