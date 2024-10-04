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
from dataclasses import dataclass
from cl.runtime.file.csv_file_reader import CsvFileReader
from cl.runtime.file.reader import Reader
from cl.runtime.schema.schema import Schema
from cl.runtime.db.protocols import DbProtocol


@dataclass(slots=True, kw_only=True)
class CsvDirReader(Reader):
    """Load records a CSV directory into the context database."""

    dir_path: str
    """Absolute path to the CSV directory where file naming convention is 'ClassName.csv'."""

    def read(self) -> None:
        # Filenames with extension but without directory path in the specified directory
        filenames = [f.name for f in os.scandir(self.dir_path) if f.is_file() and f.name.endswith(".csv")]

        # Create and run a file loader for each file
        [self._create_reader(filename).read() for filename in filenames]

    def _create_reader(self, filename: str) -> CsvFileReader:
        """Load the specified file."""

        # Obtain record type from classname which is filename without extension
        classname = filename.removesuffix(".csv")
        record_type = Schema.get_type_by_short_name(classname)  # TODO: Apply type aliases

        # Create CSV file loader
        file_path = os.path.join(self.dir_path, filename)
        loader = CsvFileReader(record_type=record_type, file_path=file_path)
        return loader
