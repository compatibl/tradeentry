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

import inspect
from dataclasses import fields, MISSING
from dataclasses import is_dataclass
from types import NoneType
from types import UnionType
from typing import Union, List, Type, Set
from typing import get_args
from typing import get_origin

from cl.runtime.log.exceptions.user_error import UserError


class RecordUtil:
    """Utilities for working with records."""

    @classmethod
    def init_all(cls, obj) -> None:
        """Invoke 'init' for each class in the order from base to derived, then validate against schema."""

        # Keep track of which init methods in class hierarchy were already called
        invoked = set()

        # Reverse the MRO to start from base to derived
        for class_ in reversed(obj.__class__.__mro__):
            class_init = getattr(class_, "init", None)
            if class_init is not None and (qualname := class_init.__qualname__) not in invoked:
                # Add qualname to invoked to prevent executing the same method twice
                invoked.add(qualname)
                # Invoke 'init' method of superclass if it exists, otherwise do nothing
                class_init(obj)

        # Perform validation against the schema only after all init methods are called
        cls.validate(obj)

    @classmethod
    def validate(cls, obj) -> None:
        """Validate against schema (invoked by init_all after all init methods are called)."""
        # TODO: Support other dataclass-like frameworks
        class_name = obj.__class__.__name__
        if is_dataclass(obj):
            for field in fields(obj):
                field_value = getattr(obj, field.name)
                if field_value is not None:
                    # Check that for the fields that have values, the values are of the right type
                    if not cls._is_instance(field_value, field.type):
                        field_type_name = cls._get_field_type_name(field.type)
                        value_type_name = type(field_value).__name__
                        if "member_descriptor" not in value_type_name:  # TODO(Roman): Remove when fixed
                            raise RuntimeError(
                                f"""Type mismatch for field '{field.name}' of class {class_name}.
Type in dataclass declaration: {field_type_name}
Type of the value: {type(field_value).__name__}
Note: In case of containers, type mismatch may be in one of the items.
"""
                            )
                else:
                    default_is_none = field.default is None
                    default_factory_is_missing = field.default_factory is MISSING
                    default_value_not_set = default_is_none and default_factory_is_missing
                    if default_value_not_set and not cls._is_optional(field.type):
                        # Error if a field is None but declared as required
                        raise UserError(f"Field '{field.name}' in class '{class_name}' is required but not set.")

    @classmethod
    def is_abstract(cls, record_type: Type) -> bool:
        """Return True if 'record_type' is abstract."""
        return bool(inspect.isabstract(record_type))

    @classmethod
    def get_non_abstract_descendants(cls, record_type: Type) -> List[Type]:
        """Find non-abstract descendants of 'record_type' to all levels and return the list of ClassName."""
        subclasses = record_type.__subclasses__()
        result = []
        for subclass in subclasses:
            # Recursively check subclasses
            result.extend(cls.get_non_abstract_descendants(subclass))
            # If the subclass is not abstract, add it to the list
            if not inspect.isabstract(subclass):
                result.append(subclass)
        return result

    @classmethod
    def _is_instance(cls, field_value, field_type) -> bool:

        origin = get_origin(field_type)
        args = get_args(field_type)

        if origin is None:
            # Not a generic type, consider the possible use of annotation
            if isinstance(field_type, type):
                return isinstance(field_value, field_type)
            elif isinstance(field_type, str):
                field_value_type_name = type(field_value).__name__
                return field_value_type_name == field_type
            else:
                raise RuntimeError(f"Field type {field_type} is neither a type nor a string.")
        elif origin in [UnionType, Union]:
            if field_value is None:
                return NoneType in args
            else:
                return any(cls._is_instance(field_value, arg) for arg in args)
        elif cls._is_instance(field_value, origin):
            # If the generic has type parameters, check them
            if args:
                if isinstance(field_value, list) and origin is list:
                    return all(cls._is_instance(item, args[0]) for item in field_value)
                elif isinstance(field_value, dict) and origin is dict:
                    return all(
                        isinstance(key, args[0]) and cls._is_instance(value, args[1])
                        for key, value in field_value.items()
                    )
        else:
            # Not an instance of the specified origin
            return False

    @classmethod
    def _is_optional(cls, field_type) -> bool:
        """Return true if None is an valid value for field_type."""
        # Check if the type is a union
        if get_origin(field_type) in [UnionType, Union]:
            # Check if NoneType is one of the arguments in the union
            return NoneType in get_args(field_type)
        else:
            # Type hint is not a union, the value cannot be None
            return False

    @classmethod
    def _get_field_type_name(cls, field_type):
        """Get the name of a type, including handling for Union types."""
        if get_origin(field_type) in [UnionType, Union]:
            return " | ".join(t.__name__ for t in get_args(field_type))
        else:
            return field_type.__name__
