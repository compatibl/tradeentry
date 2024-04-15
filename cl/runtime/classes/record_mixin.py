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

from __future__ import annotations
from abc import ABC
from typing import List, Any
from typing_extensions import Self
from cl.runtime.classes.class_info import ClassInfo
from cl.runtime.rest.context import Context


class RecordMixin(ABC):
    """
    Optional mixin class for database records providing static type checkers with method signatures.

    Those methods that raise an exception must be overridden in derived types or by a decorator.
    They are not made abstract to avoid errors from static type checkers.

    The use of this class is optional. The code must not rely on inheritance from this class.

    Records may implement handlers and/or viewers:

    - Handlers are methods that can be invoked from the UI
    - Viewers are methods whose return value is displayed in the UI
    - Both may be instance, class or static methods, and may have parameters
    """

    __slots__ = []  # Adding an empty __slots__ declaration prevents the creation of a __dict__ for every instance

    def init(self) -> None:
        """Similar to __init__ but uses previously set fields instead of parameters (not invoked by data source)."""

        # Do nothing by default
        pass

    def validate(self) -> None:
        """Validate previously set fields (invoked by data source before saving and after loading)."""

        # Do nothing by default
        pass

    @classmethod
    def load_many(
            cls: Self,
            records_or_keys: List[Any | None] | None = None,
            dataset: List[str] | str | None = None,
            *,
            context: Context = None
    ) -> List[Self | None] | None:
        """
        Load serialized records from a single table using a list of keys.
        If records are passed instead of keys, they are returned without data source lookup.

        Returns:
            Iterable of records with the same length and in the same order as the list of keys.
            A result element is None if the record is not found or the key is None.

        Args:
            records_or_keys: Each element is a record, key, semicolon-delimited string, or None.
            dataset: List of datasets in lookup order, single dataset, or None for root dataset.
            context: Optional context, if None current context will be used
        """
        return ClassInfo.load_many(cls, records_or_keys, dataset, context=context)
