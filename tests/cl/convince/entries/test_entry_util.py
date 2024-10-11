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

import pytest
from cl.runtime.testing.regression_guard import RegressionGuard
from cl.convince.entries.entry import Entry
from cl.convince.entries.entry_key import EntryKey
from cl.convince.entries.entry_util import EntryUtil


def test_create_id():
    """Test EntryKey.create_key method."""

    guard = RegressionGuard()

    # Check with type and title only
    guard.write(EntryUtil.create_id(Entry, "Sample Title"))

    # Check with body
    guard.write(EntryUtil.create_id(Entry, "Sample Title", body="Sample Body"))

    # Check with data
    guard.write(EntryUtil.create_id(Entry, "Sample Title", data="Sample Data"))

    # Check with both
    guard.write(EntryUtil.create_id(Entry, "Sample Title", body="Sample Body", data="Sample Data"))

    # Verify
    guard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
