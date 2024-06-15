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

from typing import List


class TableMixin:
    """Optional mixin for table classes."""

    __slots__ = ()
    """To prevent creation of __dict__ in derived types."""

    @classmethod
    def get_key_fields(cls) -> List[str]:
        """
        Get primary key fields by parsing the source of 'get_key' method of 'record_type'.

        Notes:
            Override in the table type in case of non-standard implementation of 'get_key' or
            non-standard name or module of the table type.
        """

        # TODO: Determine the reason for cyclic reference and move to the top of the module
        from cl.runtime.records.class_info import ClassInfo
        from cl.runtime.records.key_util import KeyUtil

        # Obtain class path by removing Table suffix from class name and _key suffix from module name
        if not cls.__module__.endswith('_key'):
            raise RuntimeError(f"Module {cls.__module__} of the table class does not end with '_key'.")
        if not cls.__name__.endswith('Table'):
            raise RuntimeError(f"Table class {cls.__name__} does not end with 'Table'.")
        class_path = f"{cls.__module__.removesuffix('_key')}.{cls.__name__.removesuffix('Table')}"

        # Load record type dynamically
        record_type = ClassInfo.get_class_type(class_path)

        # Get primary key fields by parsing the source of 'get_key' method of 'record_type'
        key_fields = KeyUtil.get_key_fields(record_type)
        return key_fields
