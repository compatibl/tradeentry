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

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from cl.runtime.records.class_info import ClassInfo
from cl.runtime.settings.config import dynaconf_settings
from cl.runtime.storage.data_source_types import TDataset, TIdentity
from cl.runtime.storage.data_source_types import TKey
from cl.runtime.storage.data_source_types import TPackedRecord
from cl.runtime.storage.data_source_types import TQuery
from cl.runtime.storage.data_source_types import TLoadedRecord
from dataclasses import dataclass
from typing import ClassVar, List
from typing import Iterable


@dataclass(slots=True)
class TypeResponse:
    """REST API response for a single item of the list returned by the /data/types route."""

    type_id: str
    """Unique type identifier using module.ClassName or another format."""

    type_label: str
    """Type label displayed in the UI, by default ClassName but may be customized in settings."""
