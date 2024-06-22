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

from typing import Literal

# TODO: Refactor
HandlerType = Literal[
    "job",  # Job handler is shown as a button, return type must be None, params are allowed
    "process",  # Process handler, return type is not allowed, params are allowed
    "viewer",  # Viewer, return type is allowed, params are allowed
    "content"  # # Viewer, return type is allowed, params not allowed
]
"""Handler type."""
