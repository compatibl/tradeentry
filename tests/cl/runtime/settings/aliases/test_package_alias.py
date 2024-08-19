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
from cl.runtime.settings.package_alias import PackageAlias


@pytest.mark.skip("Temporarily disabled during refactoring.")  # TODO: Switch to new classes and enable
def test_package_aliases():
    """Test UiSettings class."""

    api_settings = None

    assert api_settings.package_aliases == {
        "cl.runtime": "rt",
        "stubs.cl.runtime": "stubs.rt",
    }

    # Call twice to check caching
    for _ in range(2):
        assert api_settings.get_package_alias("cl") is None
        assert api_settings.get_package_alias("cl.unknown.package") is None
        assert api_settings.get_package_alias("cl.runtime") == "rt"
        assert api_settings.get_package_alias("cl.runtime.storage") == "rt"


if __name__ == "__main__":
    pytest.main([__file__])
