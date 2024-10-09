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
import os
from cl.runtime.settings.preload_settings import PreloadSettings
from cl.runtime.testing.regression_guard import RegressionGuard


def test_preload_settings():
    """Test PreloadSettings class."""

    preload_settings = PreloadSettings.instance()

    # Check that all paths exist and are absolute paths
    errors = []
    for dir_path in preload_settings.dirs:
        if not os.path.exists(dir_path):
            errors.append(f"   - Preload directory does not exist: {dir_path}\n")
        if not os.path.isabs(dir_path):
            errors.append(f"   - Preload directory path is not absolute: {dir_path}\n")
    if errors:
        raise RuntimeError("Preload directory errors:\n" + "".join(errors))


if __name__ == "__main__":
    pytest.main([__file__])

