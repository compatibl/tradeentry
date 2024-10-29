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

import csv
import os
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Type
from cl.runtime import Context
from cl.runtime.file.reader import Reader
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.primitive.char_util import CharUtil
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.schema.element_decl import ElementDecl
from cl.runtime.schema.schema import Schema
from cl.runtime.schema.type_decl import TypeDecl
from cl.runtime.serialization.dict_serializer import get_type_dict
from cl.runtime.serialization.flat_dict_serializer import FlatDictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer
from cl.runtime.serialization.string_value_parser_enum import StringValueParser

serializer = FlatDictSerializer()


@dataclass(slots=True, kw_only=True)
class CsvFileReader(Reader):
    """Load records from a single CSV file into the context database."""

    file_path: str
    """Absolute path to the CSV file including extension."""

    def read_and_save(self) -> None:
        # Get current context
        context = Context.current()

        with open(self.file_path, mode="r", encoding="utf-8") as file:
            # The reader is an iterable of row dicts
            csv_reader = csv.DictReader(file)
            row_dicts = [row_dict for row_dict in csv_reader]

            invalid_rows = set(
                index
                for index, row_dict in enumerate(row_dicts)
                for key in row_dict.keys()
                if key is None or key == ""  # TODO: Add other checks for invalid keys
            )

            if invalid_rows:
                rows_str = "".join([f"Row: {invalid_row}\n" for invalid_row in invalid_rows])
                raise RuntimeError(
                    f"Misaligned values found in the following rows of CSV file: {self.file_path}\n"
                    f"Check the placement of commas and double quotes.\n" + rows_str
                )

            # Deserialize rows into records
            records = [self._deserialize_row(row_dict) for row_dict in row_dicts]

            # Save records to the specified database
            if records:
                context.save_many(records)

    @classmethod
    def _prepare_csv_value(cls, csv_value: str, element_decl: ElementDecl):
        """Prepare csv value before deserialization."""

        # TODO (Roman): add ability to see difference between an empty string and None.
        # Replace empty string to None
        if csv_value is None or csv_value == "":
            return None

        if element_decl is None:
            raise NotImplementedError()

        if not element_decl.vector and (value_decl := element_decl.value) is not None:
            # Convert primitive types
            if value_decl.type_ == "Int":
                return int(csv_value)
            elif value_decl.type_ == "Double":
                return float(csv_value)
        elif (key := element_decl.key_) is not None and StringValueParser.parse(csv_value)[1] is None:
            # Get key type from element decl
            key_type_name = key.name
            type_dict = get_type_dict()
            key_type = type_dict.get(key_type_name)  # noqa

            # Deserialize key from string
            key_serializer = StringSerializer()
            return key_serializer.deserialize_key(csv_value, key_type)

        return csv_value

    def _deserialize_row(self, row_dict: Dict[str, Any]) -> RecordProtocol:
        """Deserialize row into a record."""

        # Record type is ClassName without extension in PascalCase
        filename = os.path.basename(self.file_path)
        filename_without_extension, _ = os.path.splitext(filename)

        if not CaseUtil.is_pascal_case(filename_without_extension):
            dirname = os.path.dirname(filename)
            raise RuntimeError(
                f"Filename of a CSV preload file {filename} in directory {dirname} must be "
                f"ClassName or its alias in PascalCase without module."
            )

        # Get record type
        record_type = Schema.get_type_by_short_name(filename_without_extension)

        # Get TypeDecl object for record type
        type_decl = TypeDecl.for_type(record_type)

        # Construct name to element decl map
        type_decl_elements = (
            {element.name: element for element in type_decl.elements} if type_decl.elements is not None else {}
        )

        prepared_row = {}
        for k, v in row_dict.items():

            # Normalize characters in both key and value
            k = CharUtil.normalize_chars(k)
            v = CharUtil.normalize_chars(v)

            # Get element_decl for field
            pascal_case_field_name = CaseUtil.snake_to_pascal_case(k)
            element_decl = type_decl_elements.get(pascal_case_field_name)

            if element_decl is None:
                raise UserError(
                    f"Field '{k}' is not defined in record '{record_type.__name__}' "
                    f"while its value '{v}' is present in CSV input."
                )

            # Prepare csv value using element decl
            prepared_row[k] = self._prepare_csv_value(v, element_decl)

        prepared_row["_type"] = record_type.__name__
        return serializer.deserialize_data(prepared_row)
