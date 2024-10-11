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
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.primitive.string_util import StringUtil
from cl.runtime.records.protocols import is_record


class EntryUtil:
    """Helper methods for the Entry class."""

    @classmethod
    def create_id(
        cls,
        type_: Type | str,
        title: str,
        *,
        body: str | None = None,
        data: str | None = None,
    ) -> str:
        """Create entry_id in 'Type: Title' format followed by an MD5 hash of body and data if present."""

        # Initial checks and conversions for type
        if isinstance(type_, type):
            # Check it is a record
            if not is_record(type_):
                raise RuntimeError(f"Parameter type_={type_.__name__} of 'create_id' method is not a record.")
            # Convert to name
            type_ = type_.__name__
        elif isinstance(type_, str):
            # Class name, ensure it has the right format
            if "." in type_:
                raise RuntimeError(f"Parameter type_={type_} of 'create_id' method must be classname without module.")
            if "\n" in type_:
                raise RuntimeError(f"Parameter type_={type_} of 'create_id' method must not contain EOL.")
            if not CaseUtil.is_pascal_case(type_):
                raise RuntimeError(f"Parameter type_={type_} of 'create_id' method is not PascalCase.")
        else:
            raise RuntimeError(f"Parameter type_={type_} of 'create_id' method is not a string or type.")

        # Initial checks and conversions for title
        if StringUtil.is_empty(title):
            raise RuntimeError("Empty 'title' parameter is passed to 'create_id' method.")
        max_title_len = 1000
        if len(title) > max_title_len:
            raise RuntimeError(
                f"The length {len(title)} of the 'title' parameter passed to 'create_id' method "
                f"exceeds the {max_title_len} limit, use body parameter for the excess text."
            )
        if "\n" in type_:
            raise RuntimeError(f"Parameter title={title} of 'create_id' method must not contain EOL.")

        # Type is ClassName without module
        entry_id = f"{type_}: {title}"

        # Append MD5 hash in hexadecimal format of the body and data if present
        if not StringUtil.is_empty(body) or not StringUtil.is_empty(data):
            md5_hash = StringUtil.md5_hex(f"{body}.{data}")
            entry_id = f"{entry_id} (MD5: {md5_hash})"
        return entry_id
