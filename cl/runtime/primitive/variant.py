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

import datetime as dt
import importlib
from enum import IntEnum
from typing import Any, Dict, Union

from cl.runtime.date_time.date_time_aggregate_util import DateTimeAggregateUtil
from cl.runtime.primitive.schema_helper import enum_name_from_schema, enum_name_to_schema
from cl.runtime.primitive.string_util import to_pascal_case, to_snake_case
from cl.runtime.primitive.variant_type import VariantType
from cl.runtime.storage.context import Context
from cl.runtime.storage.data import Data
from cl.runtime.storage.key import Key

VariantHint = Union[None, str, float, int, bool, dt.date, dt.time, dt.datetime, IntEnum, Key, Data]


def _get_wrong_type_error_message(type_: type) -> str:
    # strip typing.Union[] from available types description
    available_types = str(VariantHint).split('[', 1)[1][:-1]
    return f'Variant cannot hold {type_.__name__} type. Available types are {available_types}'


class Variant:
    """Variant type can hold any atomic value or be empty."""

    _variant_types = {str, float, int, bool, dt.date, dt.time, dt.datetime, IntEnum}
    _type_mapping: Dict[type, VariantType] = {
        float: VariantType.Double,
        str: VariantType.String,
        bool: VariantType.Bool,
        int: VariantType.Int,
        dt.date: VariantType.Date,
        dt.time: VariantType.Time,
        dt.datetime: VariantType.DateTime,
        IntEnum: VariantType.Enum,
    }
    __slots__ = ('_value',)
    _value: VariantHint

    def __init__(self, value: VariantHint):
        """Create from object of supported types, error message if argument type is unsupported."""
        if value is None:
            self._value = None
        else:
            type_ = type(value)
            if type_ in Variant._variant_types or Data in type_.__mro__ or IntEnum in type_.__mro__:
                self._value = value
            else:
                raise Exception(_get_wrong_type_error_message(type_))

    def __eq__(self, other):
        if type(other) is not Variant:
            return False
        other: Variant
        if other._value != self._value:
            return False
        return True

    def __ne__(self, other):
        if type(other) is not Variant:
            return True
        other: Variant
        if other._value != self._value:
            return True
        return False

    def value_type(self) -> VariantType:
        """Type of the value held by the variant."""
        type_ = type(self._value)
        if self._value is None:
            return VariantType.Empty

        elif type_ == str:
            return VariantType.String
        elif Key in type_.__mro__:
            return VariantType.Key
        elif Data in type_.__mro__:
            return VariantType.Data
        elif IntEnum in type_.__mro__:
            return VariantType.Enum

        variant_type = self._type_mapping.get(type_, None)
        if variant_type is not None:
            if variant_type == VariantType.Int and (self._value > 2147483647 or self._value < -2147483648):
                return variant_type.Long
            return variant_type
        else:
            raise Exception(_get_wrong_type_error_message(type_))

    def value(self) -> VariantHint:
        """Value held by the variant, which may be None."""
        return self._value

    def to_bson(self) -> Dict[str, Any]:
        """Serialize variant to bson."""

        from cl.runtime.storage.data import Data

        inner_value = self.value()
        inner_type = self.value_type()

        if inner_value is None:
            serialized_value = None
        elif inner_type in (
            VariantType.Date,
            VariantType.Time,
            VariantType.DateTime,
        ):
            serialized_value = DateTimeAggregateUtil.value_to_iso_int(inner_value)
        elif inner_type in (VariantType.Data, VariantType.Key):
            serialized_value = inner_value.to_bson(Data)
        elif inner_type == VariantType.Enum:
            enum_type = type(inner_value)
            enum_type_module = '.'.join(
                to_pascal_case(module_part) for module_part in enum_type.__module__.split('.')[:-1]
            )
            serialized_value = {
                '_t': f'{enum_type_module}.{enum_type.__name__}',
                'Value': enum_name_to_schema(inner_value),
            }
        else:
            serialized_value = inner_value

        return {inner_type.name: serialized_value}

    @classmethod
    def from_bson(cls, dict_: Dict[str, Any], context: Context = None) -> 'Variant':
        """Deserialize variant from bson."""

        if len(dict_) != 1:
            raise ValueError(f'Unexpected Variant format: {dict_}')

        variant_type_name, raw_value = next(iter(dict_.items()))
        variant_type = VariantType[variant_type_name]

        if variant_type == VariantType.Empty:
            return cls(None)

        if raw_value is None:
            raise ValueError(f'Expected variant type {variant_type.name}, got None.')

        if variant_type == VariantType.Enum:
            enum_type_module_str = raw_value['_t']
            enum_type_name = enum_type_module_str[enum_type_module_str.rfind('.') + 1 :]
            enum_type_module_str = '.'.join(
                to_snake_case(module_part) for module_part in enum_type_module_str.split('.')
            )
            enum_type_module = importlib.import_module(enum_type_module_str)
            enum_type = getattr(enum_type_module, enum_type_name)
            value = enum_name_from_schema(enum_type, raw_value['Value'])
        elif variant_type == VariantType.Long:
            value = int(raw_value)
        elif (
            variant_type == VariantType.Date or variant_type == VariantType.Time or variant_type == VariantType.DateTime
        ):
            real_type = list(cls._type_mapping.keys())[list(cls._type_mapping.values()).index(variant_type)]
            value = DateTimeAggregateUtil.value_from_iso_int(raw_value, real_type)
        elif variant_type in (VariantType.Data, VariantType.Key):
            value = Data.from_bson(raw_value, context=context)
        else:
            value = raw_value

        return cls(value)
