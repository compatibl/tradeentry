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
import re
from typing import List
from typing import Type
from uuid import UUID
import uuid_utils
from cl.runtime.exceptions.error_message_util import ErrorMessageUtil

_ISO_DELIMITED_FORMAT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z-[a-f0-9]{20}$")
"""Regex for the legacy UUIDv7-based timestamp format where the datetime component uses ISO-8601 delimiters."""


def _get_uuid7() -> UUID:
    """Get a new UUIDv7 and convert the result from uuid_utils.UUID type to uuid.UUID type."""
    return UUID(bytes=uuid_utils.uuid7().bytes)


class Timestamp:
    """
    UUIDv7 RFC-9562 based timestamp in time-ordered dash-delimited string format with additional
    strict time ordering guarantees within the same process, thread and context.
    """

    # TODO: Use context vars to prevent a race condition between contexts or threads
    _prev_uuid7 = _get_uuid7()
    """The last UUIDv7 created during the previous call within the same context."""

    @classmethod
    def create(cls) -> str:
        """
        Within the same process, thread and context the returned value is greater than any previous values.
        In all other cases, the value is unique and greater than values returned in prior milliseconds.
        """

        # TODO: Multiple context or threads are not yet supported

        # Keep getting new uuid7 until it is more than '_prev_uuid7'
        # At worst this will delay execution by one time tick only
        while (current_uuid7 := _get_uuid7()) <= cls._prev_uuid7:
            pass

        # Update _prev_uuid7 with the result to ensure strict ordering within the same process thread and context
        cls._prev_uuid7 = current_uuid7
        result = cls.from_uuid7(current_uuid7)
        return result

    @classmethod
    def create_many(cls, count: int) -> List[str]:
        """
        Within the same process, thread and context returned values are ordered and greater than any previous values.
        In all other cases, the returned values are ordered and greater than values returned in prior milliseconds.
        """
        # TODO: Improve performance of create_many by getting many values at the same time and ordering them
        return [cls.create() for _ in range(count)]

    @classmethod
    def from_uuid7(cls, value: UUID) -> str:
        """Convert UUIDv7 to the string Timestamp format."""
        # Validate
        cls.validate_uuid7(value)

        # Get the hexadecimal representation of the UUID
        uuid_hex = value.hex

        # Extract the first 12 hex digits representing the timestamp
        timestamp_hex = uuid_hex[:12]

        # Convert the hex timestamp to an integer (milliseconds since epoch)
        timestamp_ms = int(timestamp_hex, 16)

        # Convert milliseconds to a datetime object
        datetime_obj = dt.datetime.utcfromtimestamp(timestamp_ms / 1000.0)

        # Format the datetime to time-ordered dash-delimited string format with millisecond precision
        datetime_str = datetime_obj.strftime("%Y-%m-%d-%H-%M-%S-%f")[:-3]

        # Append the remaining part of the UUID
        remaining_uuid = uuid_hex[12:]

        # Combine the ISO datetime with the remaining UUID part
        result = f"{datetime_str}-{remaining_uuid}"
        return result

    @classmethod
    def to_datetime(
        cls,
        timestamp: str,
        *,
        value_name: str | None = None,
        method_name: str | None = None,
        data_type: Type | str | None = None,
    ) -> dt.datetime:
        """
        Return the UTC datetime component of a UUIDv7 based timestamp time-ordered dash-delimited string format.

        Args:
            timestamp: UUIDv7 based timestamp in time-ordered format yyyy-MM-dd-hh-mm-ss-fff-hex(20)
            value_name: Variable, field or parameter name for formatting the error message (optional)
            method_name: Method or function name for formatting the error message (optional)
            data_type: Class type or name for formatting the error message (optional)
        """

        # Provide a specific error message for the ISO-delimited legacy format
        if len(timestamp) == 45 and re.match(_ISO_DELIMITED_FORMAT_RE, timestamp):
            value_description = ErrorMessageUtil.value_caused_an_error(
                timestamp,
                value_name=value_name if value_name is not None else "Timestamp",
                method_name=method_name,
                data_type=data_type,
            )
            raise RuntimeError(
                f"""{value_description}
- It uses legacy format with ISO-8601 delimiters for the datetime component: yyyy-MM-ddThh:mm:ss.fffZ-hex(20)
- Convert to the new format by replacing all delimiters by dash so that the timestamp can be used in filenames
- New format example: yyyy-MM-dd-hh-mm-ss-fff-hex(20)
"""
            )

        # Validate
        tokens = timestamp.split("-")
        if len(timestamp) != 44 or len(tokens) != 8:
            value_description = ErrorMessageUtil.value_caused_an_error(
                timestamp,
                value_name=value_name if value_name is not None else "Timestamp",
                method_name=method_name,
                data_type=data_type,
            )
            raise RuntimeError(
                f"""{value_description}
- The value does not conform to the expected format yyyy-MM-dd-hh-mm-ss-fff-hex(20)
- It has {len(tokens)} dash-delimited tokens instead of 8
"""
            )

        year, month, day, hour, minute, second, millisecond, suffix = tuple(tokens)

        # Create datetime, this also validates the inputs
        try:
            # Create the date component
            result = dt.datetime(
                int(year),
                int(month),
                int(day),
                int(hour),
                int(minute),
                int(second),
                1000 * int(millisecond),
                tzinfo=dt.timezone.utc,
            )
            # Validate the hex component
            if len(suffix) != 20:
                raise ValueError(f"Hex component of UUIDv7 timestamp '{timestamp}' does not have length 20.")
            if not suffix.startswith("7"):
                raise ValueError(f"Hex component of UUIDv7 timestamp '{timestamp}' does not start from 7.")
        except ValueError as e:
            value_description = ErrorMessageUtil.value_caused_an_error(
                timestamp,
                value_name=value_name if value_name is not None else "Timestamp",
                method_name=method_name,
                data_type=data_type,
            )
            raise RuntimeError(
                f"""{value_description}
- The value does not conform to the expected format yyyy-MM-dd-hh-mm-ss-fff-hex(20)
- It causes the following parsing error:
{e}
"""
            )
        return result

    @classmethod
    def validate(
        cls,
        timestamp: str,
        *,
        value_name: str | None = None,
        method_name: str | None = None,
        data_type: Type | str | None = None,
    ) -> None:
        """
        Validate that the argument is a UUIDv7 based timestamp in time-ordered dash-delimited string format.

        Args:
            timestamp: UUIDv7 based timestamp in time-ordered format yyyy-MM-dd-hh-mm-ss-fff-hex(20)
            value_name: Variable, field or parameter name for formatting the error message (optional)
            method_name: Method or function name for formatting the error message (optional)
            data_type: Class type or name for formatting the error message (optional)
        """
        # Use validation in to_datetime method and discard the result
        cls.to_datetime(
            timestamp,
            value_name=value_name,
            method_name=method_name,
            data_type=data_type,
        )

    @classmethod
    def validate_uuid7(cls, value: UUID) -> None:
        """Validate that the argument is a valid UUIDv7."""

        # Check type
        if (value_type_name := type(value).__name__) != "UUID":
            raise RuntimeError(f"An object of type '{value_type_name}' was provided while UUIDv7 was expected.")

        # Check version
        if value.version != 7:
            raise RuntimeError(f"UUID v{value.version} was provided while v7 was expected.")
