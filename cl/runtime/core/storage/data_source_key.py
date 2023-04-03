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

from dataclasses import dataclass

from cl.runtime.core.storage.class_data import class_field
from cl.runtime.core.storage.class_record import ClassRecord


@dataclass
class DataSourceKey(ClassRecord):
    """
    Data source is a storage API for polymorphic, hierarchical data that
    can be implemented for a NoSQL DB, relational DB, key-value store,
    cloud storage, in-memory cache, distributed cache, or a filesystem.

    On top of the storage layer, the API adds a directory-like attribute
    called the dataset.

    The data source API provides the ability to:

    * Query the list of datasets;
    * Store and query records in a specific dataset; and
    * Query records across multiple datasets using dataset priority order.
    """

    data_source_id: str = class_field()
    """Unique data source identifier."""

    def to_pk(self) -> str:
        """Return primary key (PK) as string."""
        return f'rt.DataSource;{self.data_source_id}'
