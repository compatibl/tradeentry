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
from pathlib import Path
from cl.runtime.settings.project_settings import ProjectSettings


def test_project_settings():
    """Test ProjectSettings class."""

    # Relative to the location of this test module
    two_level_root_dir = os.path.normpath(Path(__file__).parents[6])
    one_level_root_dir = os.path.normpath(Path(__file__).parents[5])

    # Create settings
    project_settings = ProjectSettings.instance()

    # Check project root
    if ProjectSettings.project_levels == 1:
        assert project_settings.project_root == two_level_root_dir
        assert project_settings.get_package_root("cl.runtime") == project_settings.project_root
        assert project_settings.get_source_root("cl.runtime") == os.path.normpath(
            os.path.join(project_settings.project_root, "cl", "runtime")
        )
    elif project_settings.project_levels == 2:
        assert project_settings.project_root == one_level_root_dir
        assert project_settings.get_package_root("cl.runtime") == os.path.normpath(
            os.path.join(project_settings.project_root, "runtime")
        )
        assert project_settings.get_source_root("cl.runtime") == os.path.normpath(
            os.path.join(project_settings.project_root, "runtime", "cl", "runtime")
        )
    else:
        raise RuntimeError(f"ProjectSettings.project_levels={project_settings.project_levels} is not 1 or 2.")


if __name__ == "__main__":
    pytest.main([__file__])
