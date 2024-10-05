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
import os
from pathlib import Path

import pytest
from cl.runtime.settings.project_settings import ProjectSettings


def test_project_settings():
    """Test ProjectSettings class."""

    # Relative to the location of this test module
    superproject_root_dir = os.path.normpath(Path(__file__).parents[6])
    monorepo_root_dir = os.path.normpath(Path(__file__).parents[5])

    # Create settings
    project_settings = ProjectSettings.instance()

    # Check root_dir and offset
    if project_settings.root_offset == 0:
        assert project_settings.root_dir == superproject_root_dir
    elif project_settings.root_offset == 1:
        assert project_settings.root_dir == monorepo_root_dir
    else:
        raise RuntimeError(f"ProjectSettings.root_offset={project_settings.root_offset} is not 0 or 1.")


if __name__ == "__main__":
    pytest.main([__file__])
