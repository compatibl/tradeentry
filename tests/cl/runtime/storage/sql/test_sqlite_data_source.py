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
from cl.runtime.storage.sql.sqlite_data_source import SqliteDataSource
from stubs.cl.runtime import StubDataclassRecord


def test_save_many():
    data_source = SqliteDataSource(data_source_id="default")
    record = StubDataclassRecord()

    data_source.save_many([record, record])


if __name__ == '__main__':
    test_save_many()