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
import uuid_utils
from typing import Iterable, cast
from uuid import UUID


def _get_uuid7() -> UUID:
    """Get a new UUIDv7 and convert the result from uuid_utils.UUID type to uuid.UUID type."""
    return UUID(bytes=uuid_utils.uuid7().bytes)


class OrderedUuid:
    """
    Utility class for time-ordered UUIDv7 RFC-9562 with additional strict ordering guarantees
    within the same process, thread and context.
    """

    # TODO: Use context vars to prevent a race condition between contexts or threads
    _prev_uuid = _get_uuid7()
    """The last UUID created during the previous call within the same context."""

    @classmethod
    def create_one(cls) -> UUID:
        """
        Within the same process, thread and context the returned value is greater than any previous values.
        In all other cases, the value is unique and greater than values returned in prior milliseconds.
        """

        # TODO: Multiple context or threads are not yet supported

        # Keep getting new uuid7 until it is more than '_prev_uuid'
        # At worst this will delay execution by one time tick only
        while (result := _get_uuid7()) <= cls._prev_uuid:
            pass

        # Update _prev_uuid with the result to ensure strict ordering within the same process thread and context
        _prev_uuid = result
        return result

    @classmethod
    def create_many(cls, count: int) -> Iterable[UUID]:
        """
        Within the same process, thread and context returned values are ordered and greater than any previous values.
        In all other cases, the returned values are ordered and greater than values returned in prior milliseconds.
        """
        # TODO: Improve performance of create_many by getting many values at the same time and ordering them
        return [cls.create_one() for _ in range(count)]

    @classmethod
    def datetime_of(cls, value: UUID) -> dt.datetime:
        """Return datetime of a single UUIDv7 value."""
        # Field 'UUID.timestamp' is int milliseconds while 'fromtimestamp' method expects float seconds, divide by 1000
        return dt.datetime.fromtimestamp(uuid_utils.UUID(bytes=value.bytes).timestamp / 1000, dt.timezone.utc)
