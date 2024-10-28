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
from cl.runtime.exceptions.error_message_util import ErrorMessageUtil
from cl.runtime.log.exceptions.user_error import UserError


class ColonAndSpaceDelimitedUtil:
    """Utilities for detecting and reporting disallowed characters in colon-and-space-delimited identifiers."""

    @classmethod
    def validate(
        cls,
        value: str,
        token_count: int,
        *,
        value_name: str | None = None,
        method_name: str | None = None,
        data_type: Type | str | None = None,
    ) -> None:
        """Error message if the value does not have exactly 'token_count' colon-and-space-delimited tokens."""
        tokens = value.split(": ")
        if len(tokens) != token_count:
            if token_count > 1:
                msg = ErrorMessageUtil.value_caused_an_error(
                    value,
                    value_name=value_name if value_name is not None else "a colon-and-space-delimited identifier",
                    method_name=method_name,
                    data_type=data_type,
                )
                raise UserError(
                    f"""{msg}
It must contain exactly {token_count} colon-and-space-delimited tokens.
The likely reason is that one of the constituent tokens already
contains the colon-and-space-delimiter.
"""
                )
            elif token_count == 1:
                msg = ErrorMessageUtil.value_caused_an_error(
                    value,
                    value_name=(
                        value_name
                        if value_name is not None
                        else "a single token of a colon-and-space-delimited identifier"
                    ),
                    method_name=method_name,
                    data_type=data_type,
                )
                raise UserError(f"{msg}\nIt must not contain the colon-and-space-delimiter.\n")
            else:
                raise RuntimeError(f"Token count {token_count} must be 1 or higher.")
