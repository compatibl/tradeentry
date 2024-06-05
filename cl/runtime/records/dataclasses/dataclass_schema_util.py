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

from typing import Type
from cl.runtime.records.schema_util import SchemaUtil
from cl.runtime.schema.type_decl import TypeDecl


class DataclassSchemaUtil:
    """Helper class for generating a schema for dataclass records."""

    @staticmethod
    def get_type_decl(record_type: Type) -> TypeDecl:
        """Get type declaration."""

        # Get type declaration without the data specific to the dataclass framework
        type_decl = SchemaUtil.get_type_decl(record_type)

        # Get elements into a dictionary
        element_dict = {e.name: e for e in type_decl.elements}


        return type_decl