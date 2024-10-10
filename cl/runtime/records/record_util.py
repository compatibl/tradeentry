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

from dataclasses import is_dataclass, fields
from types import UnionType
from typing import get_origin, get_args


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
                        raise RuntimeError(f"Field '{field.name}' is declared with type '{field_type_name}' "
                                           f"while its value has type '{type(field_value).__name__}'")
                elif field.default is not None:
                    # Error if a field is None but declared as required
                    raise RuntimeError(f"Field '{field.name}' in class '{class_name}' is required but not set.")

    @classmethod
    def _is_instance(cls, field_value, field_type):
        origin = get_origin(field_type)
        args = get_args(field_type)

        if origin is None:
            # Not a generic type
            return isinstance(field_value, field_type)
        elif isinstance(field_value, origin):
            # If the generic has type parameters, check them
            if args:
                if isinstance(field_value, list) and origin is list:
                    return all(isinstance(item, args[0]) for item in field_value)
                elif isinstance(field_value, dict) and origin is dict:
                    return all(
                        isinstance(key, args[0]) and isinstance(value, args[1]) for key, value in field_value.items()
                    )
        elif origin is UnionType and any(isinstance(field_value, args) for args in args):
            return True
        else:
            # Not an instance of the specified origin
            return False

    @classmethod
    def _get_field_type_name(cls, field_type):
        """Get the name of a type, including handling for Union types."""
        if get_origin(field_type) is UnionType:
            return ' | '.join(t.__name__ for t in get_args(field_type))
        else:
            return field_type.__name__
