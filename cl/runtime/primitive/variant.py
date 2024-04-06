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
from cl.runtime.primitive.variant_type import VariantType
from cl.runtime.storage.data_mixin import DataMixin
from cl.runtime.storage.key_mixin import KeyMixin
from enum import IntEnum
from typing import Dict
from typing import Union

VariantHint = Union[None, str, float, int, bool, dt.date, dt.time, dt.datetime, IntEnum, KeyMixin, DataMixin]


def _get_wrong_type_error_message(type_: type) -> str:
    # strip typing.Union[] from available types description
    available_types = str(VariantHint).split("[", 1)[1][:-1]
    return f"Variant cannot hold {type_.__name__} type. Available types are {available_types}"


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
    __slots__ = ("_value",)
    _value: VariantHint

    def __init__(self, value: VariantHint):
        """Create from object of supported types, error message if argument type is unsupported."""
        if value is None:
            self._value = None
        else:
            type_ = type(value)
            if type_ in Variant._variant_types or DataMixin in type_.__mro__ or IntEnum in type_.__mro__:
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
        elif KeyMixin in type_.__mro__:
            return VariantType.Key
        elif DataMixin in type_.__mro__:
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
