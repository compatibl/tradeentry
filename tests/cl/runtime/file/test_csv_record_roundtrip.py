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

import pytest
from pathlib import Path
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Type
import pandas as pd
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.file.csv_file_reader import CsvFileReader
from cl.runtime.records.protocols import RecordProtocol
from cl.runtime.records.protocols import is_key
from cl.runtime.serialization.flat_dict_serializer import FlatDictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer
from stubs.cl.runtime import StubDataclassDerivedFromDerivedRecord, StubDataclassComposite
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassDictFields
from stubs.cl.runtime import StubDataclassDictListFields
from stubs.cl.runtime import StubDataclassListDictFields
from stubs.cl.runtime import StubDataclassListFields
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassOptionalFields
from stubs.cl.runtime import StubDataclassOtherDerivedRecord
from stubs.cl.runtime import StubDataclassPrimitiveFields
from stubs.cl.runtime import StubDataclassRecord

flat_serializer = FlatDictSerializer()
"""Serializer for file serialization."""

key_serializer = StringSerializer()
"""Serializer for keys."""


stub_entries: List[List[RecordProtocol]] = [  # noqa
    [StubDataclassRecord(id=f"abc1_n{i}") for i in range(5)],
    [StubDataclassNestedFields(id=f"abc2_n{i}") for i in range(5)],
    [StubDataclassComposite(primitive=f"abc{i}") for i in range(5)],
    [StubDataclassDerivedRecord(id=f"abc3_n{i}") for i in range(5)],
    [StubDataclassDerivedFromDerivedRecord(id=f"abc4_n{i}") for i in range(5)],
    [StubDataclassOtherDerivedRecord(id=f"abc5_n{i}") for i in range(5)],
    [StubDataclassOptionalFields(id=f"abc7_n{i}") for i in range(5)],
    # TODO(Roman): Restore after supporting dt.date and dt.time for Mongo
    # [StubDataclassListFields(id=f"abc6_n{i}") for i in range(5)],
    # [StubDataclassDictFields(id=f"abc8_n{i}") for i in range(5)],
    # [StubDataclassDictListFields(id=f"abc9_n{i}") for i in range(5)],
    # [StubDataclassListDictFields(id=f"abc10_n{i}") for i in range(5)],
    # [StubDataclassPrimitiveFields(key_str_field=f"abc11_n{i}") for i in range(5)],
]
"""Stub entries for testing."""


def save_records_to_csv(records: Iterable, file_path: str) -> None:
    """Save records to file with specified path."""

    # Serialize records with flat serializer but use StringSerializer for keys
    record_dicts = []
    for rec in records:
        serialized_record = flat_serializer.serialize_data(rec, is_root=True)
        serialized_record.pop("_type", None)
        serialized_record_with_str_keys = {}
        for k, v in serialized_record.items():
            if is_key(key_v := getattr(rec, k, None)):
                serialized_record_with_str_keys[k] = key_serializer.serialize_key(key_v)
            else:
                serialized_record_with_str_keys[k] = v

        record_dicts.append(serialized_record_with_str_keys)

    # Use pandas df to transform list of dicts to table format and write to file
    df = pd.DataFrame(record_dicts)
    df.to_csv(file_path, index=False)


def save_test_records(entries: List[RecordProtocol]) -> Tuple[List[RecordProtocol], Path]:
    file_path = Path(__file__).parent.joinpath(f"{entries[0].__class__.__name__}.csv")
    save_records_to_csv(entries, str(file_path.absolute()))
    return entries, file_path


def read_records_from_csv(file_path: Path, entry_type: Type[RecordProtocol]):
    loader = CsvFileReader(file_path=str(file_path.absolute()))
    loader.read_and_save()


def test_roundtrip():

    with TestingContext() as context:
        for test_entries in (*stub_entries,):
            file_path = None
            try:
                expected_entries, file_path = save_test_records(test_entries)
                entry_type = type(expected_entries[0])

                read_records_from_csv(file_path, entry_type)

                actual_records = list(context.load_all(entry_type))

                assert actual_records == expected_entries
            finally:
                if file_path is not None:
                    file_path.unlink(missing_ok=True)


if __name__ == "__main__":
    pytest.main([__file__])
