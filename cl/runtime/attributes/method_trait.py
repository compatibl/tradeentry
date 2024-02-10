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


class MethodTrait(IntEnum):
    """Method traits."""

    DeclareOnly = 0
    """Used to specify handler without implementation."""

    Hidden = 1
    """
    If this flag is set, handler will be hidden in the user interface
    except in developer mode.
    """

    InteractiveInput = 2
    """Interactive Input"""

    IsAsync = 3
    """Use the flag to specify that a handler is asynchronous."""

    Override = 4
    """
    True if this implementation is an override of the
    implementation in base class.

    If this flag is false or not set, and base class
    provides implementation of the same handler, an
    error message will result.
    TODO: is obsolete?
    """
