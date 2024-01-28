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

import os
from typing import Final, Sequence
import dynaconf

CL_RUNTIME_SETTINGS_FILE: Final[str] = 'settings.json'
"""Settings file name."""

CL_RUNTIME_SETTINGS_ENV: Final[str] = os.environ.get('CL_RUNTIME_SETTINGS_ENV', 'default')
"""Name of settings environment which should be used."""

settings = dynaconf.Dynaconf(
    settings_files=CL_RUNTIME_SETTINGS_FILE,
    environments=True,
    env=CL_RUNTIME_SETTINGS_ENV,
)

CL_RUNTIME_MODULES: Final[Sequence[str]] = settings.get('CL_RUNTIME_MODULES', ['cl.runtime'])
"""Modules visible to Runtime."""

CL_RUNTIME_DB_NAME: Final[str] = settings.get('CL_RUNTIME_DB_NAME')
"""DB name."""

CL_RUNTIME_DB_PATTERN: Final[str] = settings.get('CL_RUNTIME_DB_PATTERN')
"""DB search pattern."""

CL_RUNTIME_DB_DRIVER_NAME: Final[str] = settings.get('CL_RUNTIME_DB_DRIVER_NAME')
"""DB driver name."""

CL_RUNTIME_DB_DRIVER_VERSION: Final[str] = settings.get('CL_RUNTIME_DB_DRIVER_VERSION')
"""DB driver version."""

CL_RUNTIME_WORKERS_COUNT: Final[int] = int(settings.get('CL_RUNTIME_WORKERS_COUNT'))
"""Number of handler and viewer workers to be spawned."""
