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

import uuid_utils
import datetime as dt

# TODO: Implement create_many

class UuidUtil:
    """
    Utility class for time-ordered UUIDv7 RFC-9562 with additional strict ordering guarantees
    within the same process, thread and context.
    """

    # TODO: Use context vars to prevent a race condition between contexts or threads
    _prev_uuid = uuid_utils.uuid7()
    """The last UUID created during the previous call within the same context."""

    @classmethod
    def create_one(cls) -> uuid_utils.UUID:
        """
        Return UUIDv7 with strict order guarantee within the same process, thread and context.
        In all other cases, ordering is guaranteed within timestamp resolution.
        """

        # TODO: Multiple context or threads are not yet supported

        # Keep getting new uuid7 until it is more than '_prev_uuid'
        # At worst this will delay execution by one time tick only
        while (result := uuid_utils.uuid7()) <= cls._prev_uuid:
            pass

        # Update _prev_uuid with the result to ensure strict ordering within the same process thread and context
        _prev_uuid = result
        return result

    @classmethod
    def datetime_of(cls, value: uuid_utils.UUID) -> dt.datetime:
        """Return datetime of a single UUIDv7 value."""
        # Field 'timestamp' is in milliseconds while 'fromtimestamp' expects seconds, divide by 1000
        return dt.datetime.fromtimestamp(value.timestamp / 1000, dt.timezone.utc)
