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
from typing import Optional

from cl.runtime.storage.cl_data_class_record import ClDataClassRecord


@dataclass
class ClDataSourceKey(ClDataClassRecord):
    """Key for the data source record.

    Data source is a logical concept similar to database
    that can be implemented for a document DB, relational DB,
    key-value store, or filesystem. On top of the core
    storage layer, it adds directory-like attribute called
    dataset.

    Data source API provides the ability to:

    (a) store and query datasets;
    (b) store records in a specific dataset; and
    (c) query record across a group of datasets.

    This record is always stored in root dataset.
    """

    data_source_id: Optional[str] = None
    """Unique data source identifier."""

    def to_pk(self) -> str:
        """Return primary key (PK) as string."""
        return f'rt.DataSource;{self.data_source_id}'
