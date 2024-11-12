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

from collections import defaultdict
from pathlib import Path
from typing import DefaultDict
from typing import Iterable
from typing import Type
from urllib import parse
import pandas as pd
from pydantic import BaseModel
from cl.runtime import Context
from cl.runtime.db.protocols import TRecord
from cl.runtime.file.file_util import FileUtil
from cl.runtime.routers.storage.save_permanently_request import SavePermanentlyRequest
from cl.runtime.schema.schema import Schema
from cl.runtime.serialization.flat_dict_serializer import FlatDictSerializer
from cl.runtime.serialization.string_serializer import StringSerializer


def get_type_to_records_map(request: SavePermanentlyRequest) -> DefaultDict[Type, TRecord]:
    """Fetch records from the database and return them."""

    request_type = Schema.get_type_by_short_name(request.type)
    key_serializer = StringSerializer()

    key_objs = [key_serializer.deserialize_key(key, request_type.get_key_type()) for key in request.keys]
    records = Context.current().load_many(key_objs, ignore_not_found=True)

    # TODO (Bohdan): Implement with_dependencies logic.
    # if request.with_dependencies:
    #     key_objs = [
    #         dag_node.data.node_data_reference
    #         for record in records.values()
    #         for dag_node in Dag.create_data_connection_dag_from_record(data=record).nodes
    #         if dag_node.data.node_data_reference
    #     ]
    #     records = context.load_many(key_objs, ignore_not_found=True)

    type_to_records_map = defaultdict(list)
    for record in records:
        if record:
            type_to_records_map[type(record)].append(record)

    return type_to_records_map


class SavePermanentlyResponse(BaseModel):

    @classmethod
    def _get_extension(cls) -> str:
        """Return an extension in which records should be saved."""

        # TODO (Bohdan): Check if it makes sense to have a config which format/extension to use.
        #  If not - simplify the code.
        return "csv"

    @classmethod
    def _get_path_to_save_permanently_folder(cls) -> Path:
        """Return a path to a save permanently directory."""

        # TODO (Sasha): Provide a proper path to a save permanently folder instead of the current directory
        return Path()

    @classmethod
    def _write_records(cls, file_path: Path, records: Iterable[TRecord]) -> None:
        """Write serialized records on the disk."""

        file_extension = file_path.stem

        serializer = FlatDictSerializer()  # TODO (Bohdan): Provide a proper serializer
        serialized_records = [serializer.serialize_data(record) for record in records]

        if file_extension == "csv":
            df = pd.DataFrame([serialized_records])
            df.to_csv(file_path, mode="w", index=False, header=True)
        else:
            raise ValueError(f"File extension {file_extension} is not supported.")

    @classmethod
    def save_permanently(cls, request: SavePermanentlyRequest) -> "SavePermanentlyResponse":
        """Save records to the database on the disk."""

        for record_type, records in get_type_to_records_map(request).items():
            filename = f"{record_type.__name__}.{cls._get_extension()}"
            FileUtil.check_valid_filename(filename)
            file_path = cls._get_path_to_save_permanently_folder() / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)

            cls._write_records(file_path, records)

        return SavePermanentlyResponse()
