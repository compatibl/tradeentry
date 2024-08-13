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
from cl.runtime.settings.ui_settings import UiSettings


@pytest.mark.skip("Temporarily disabled during refactoring.")  # TODO: Enable
def test_smoke():
    """Test UiSettings class."""

    ui_settings = UiSettings.instance()

    assert ui_settings.package_labels == {
        "rt": "Runtime",
        "stubs.rt": "Runtime Stubs",
    }
    assert ui_settings.type_labels == {
        "SampleClass": "Sample Class Label",
    }
    assert ui_settings.field_labels == {
        "sample_field": "Sample Field Label",
    }
    assert ui_settings.method_labels == {
        "sample_method": "Sample Method Label",
    }
    assert ui_settings.enum_item_labels == {
        "SAMPLE_ITEM": "Sample Item Label",
    }


if __name__ == "__main__":
    pytest.main([__file__])
