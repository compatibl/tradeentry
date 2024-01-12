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
    Optional mixin class for database records providing static type checkers with method signatures.

    Those methods that raise an exception must be overridden in derived types or by a decorator.
    They are not made abstract to avoid errors from static type checkers.

    The use of this class is optional. The code must not rely on inheritance from this class.

    Records may implement handlers and/or viewers:

    - Handlers are methods that can be invoked from the UI
    - Viewers are methods whose return value is displayed in the UI
    - Both may be instance, class or static methods, and may have parameters
    """

    __slots__ = []
    """Adding empty __slots__ prevents creation of __dict__ for every instance."""

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
