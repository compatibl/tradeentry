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

# TODO (Roman): use ui serialization, probably this file will be deprecated

from __future__ import annotations
import base64
from dataclasses import asdict
from dataclasses import fields
from dataclasses import is_dataclass
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.schema.field_decl import primitive_types  # TODO: Move definition to a separate module


def to_record_dict(node):  # TODO: Apply type hints
    """Recursively apply record dictionary conventions to the argument dictionary."""

    node_type = type(node)
    if node_type is bytes:
        return base64.b64encode(node).decode()
    elif node_type in primitive_types:
        # Primitive type, serialize as string
        # TODO: Apply custom formatting
        result = node
        return result
    elif issubclass(node_type, Enum):
        return node.name
    elif node_type is list:
        # TODO: !!! Generally should not skip nodes that have the value of None
        return [to_record_dict(v) for v in node if v is not None]
    elif node_type is tuple:
        # TODO: Decision on short name alias
        # Tuple key, table name is class name
        table = node[0].__name__
        result = ";".join([table] + node[1:])
        return result
    elif node_type is dict:
        # TODO: Decision on short name alias
        # Tuple key, table name is class name
        result = {k: to_record_dict(v) for k, v in node.items()}
        return result
    elif node_type.__name__.endswith("Key"):
        # Key type, use semicolon-delimited serialization
        # TODO: Do not use a method from dataclasses
        node_dict = asdict(node)
        result = ";".join(node_dict.keys())
        return result
    elif hasattr(node, "get_key") or is_dataclass(node):
        # Record or data
        # Creating the result dictionary starting with the "_t" field
        result = {"_t": node.__class__.__name__}
        for field in fields(node):
            if (value := getattr(node, field.name)) is not None:
                result[field.name] = to_record_dict(value)
        return result
    else:
        return node


def to_legacy_dict(node: Dict[str, Any] | List[Dict[str, Any]] | str) -> Dict[str, Any] | List[Dict[str, Any]] | str:
    """Recursively apply record dictionary conventions to the argument dictionary."""

    if isinstance(node, dict):
        # Skip nodes that have the value of None
        # Remove suffix _ from field names if present
        # Fields that cannot be serialized in common way
        special_fields = {'id_': 'Id_', '_t': '_t'}
        result = {
            CaseUtil.snake_to_pascal_case(k.removesuffix("_")) if not k in special_fields else special_fields[k]:
            to_legacy_dict(v)
            for k, v in node.items()
            if v is not None
        }
        return result
    elif isinstance(node, list):
        # Skip nodes that have the value of None
        return [to_legacy_dict(v) for v in node if v is not None]
    elif isinstance(node, tuple):
        # TODO: Decision on short alias
        # Tuple key, remove Key suffix from key type to obtain table name
        table = node[0].__name__
        result = ";".join([table] + node[1:])
        return result
    else:
        return node
