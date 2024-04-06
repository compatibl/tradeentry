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
from cl.runtime.storage.key_mixin import KeyMixin
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

TRecord = TypeVar("TRecord", bound=KeyMixin)


def index_fields(definition: str, name: str = None):
    """
    Use index_fields decorator to specify database indexes
    for the class. A class may have more than one index_fields
    decorator, each for a separate index.

    This method must be set for the root data type of a collection.
    Root data type is the type derived directly from TypedRecord.

    The definition string for the index is a comma separated
    list of element names. The elements sorted in descending
    order are prefixed by -.

    Examples:

    * A is an index on element A in ascending order;
    * -A is an index on element A in descending order;
    * A,B,-C is an index on elements A and B in ascending
      order and then element C in descending order.

    When collection interface is obtained from a data source,
    names of the elements in the index definition are validated
    to match element names of the class for which the index is
    defined. If the class does not have an element with the
    name specified as part of the definition string, an error
    message is given.
    """

    def wrap(cls: Type[TRecord]):
        if not inspect.isclass(cls):
            raise Exception("@index_fields should be applied on class")
        if KeyMixin not in cls.__mro__:
            raise Exception("@index_fields should be applied on Record derived class")

        # Set _has_index_fields attribute
        if not hasattr(cls, "_has_index_fields"):
            cls._has_index_fields = True

        # Add index elements list to cls
        if "_index_fields" not in cls.__dict__:
            cls._index_fields = list()

        # Remove + prefix from definition if specified
        index_definition = definition if not definition.startswith("+") else definition[1:]
        index_name = name
        index = (index_definition, index_name)

        # Add index element to list
        cls._index_fields.append(index)
        return cls

    return wrap


def get_index_fields_dict(cls: Type[TRecord]) -> Dict[str, Dict[str, Any]]:
    """
    Get index fields for the class and its parents as Dict[IndexDefinition, IndexName].
    """

    # The dictionary uses definition as key and name as value;
    # the name is the same as definition unless specified in
    # the attribute explicitly.
    result: Dict[str, Dict[str, Any]] = dict()

    # Check if index elements exists
    if not getattr(cls, "_has_index_fields", False):
        return result

    # Iterate over base classes and extract index elements
    for base_cls in filter(lambda x: "_index_fields" in x.__dict__, cls.__mro__):
        for index_def, index_name in base_cls._index_fields:  # type: str, str
            prev_value = result.setdefault(index_def, {"index_name": index_name})

            # If already included, check that the name matches, error message otherwise
            if prev_value["index_name"] != index_name:
                raise Exception(
                    f"The same index definition {index_def} is provided with two different "
                    f'custom index names {index_name} and {prev_value["index_name"]} in the inheritance chain '
                    f"for class {cls.__name__}."
                )

    return result
