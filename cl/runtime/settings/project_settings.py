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

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from typing_extensions import Self
from cl.runtime.records.dataclasses_extensions import missing


@dataclass(slots=True, kw_only=True)
class ProjectSettings:
    """
    Information about the project location and layout (used to search for settings and submodules).

    Notes:
        - This class is used to search for .env or settings.yaml
        - It does not read data .env or settings.yaml because its initialization happens before
    """

    root_dir: str = missing()
    """
    Superproject root if contains .env or settings.yaml, otherwise monorepo root if contains one of these files.
    + Superproject root
        ++ component_1
            +++ (files for component_1)
        ++ component_2
            +++ (files for component_2)     
    OR
    + Monorepo root
        ++ (files for component_1)
        ++ (files for component_2)
    """

    root_offset: int = missing()
    """One for superproject or zero for monorepo layout."""
    
    __instance: ClassVar[ProjectSettings] = None
    """Singleton instance."""

    @classmethod
    def instance(cls) -> Self:
        """Return singleton instance."""
        # Check if cached value exists, load if not found
        if cls.__instance is None:
            # Possible project root locations for each layout relative to this module
            superproject_root_dir = os.path.normpath(Path(__file__).parents[4])
            monorepo_root_dir = os.path.normpath(Path(__file__).parents[3])
            
            # Settings filenames to search
            settings_filenames = [".env", "settings.yaml"]

            root_dir = None
            root_offset = None
            try:
                if os.path.exists(superproject_root_dir):
                    # Supermodule directory takes priority but only if it contains one of the settings files
                    if any(os.path.exists(os.path.join(superproject_root_dir, x)) for x in settings_filenames):
                        root_dir = superproject_root_dir
                        root_offset = 1
            # Handle the possibility that directory access is prohibited
            except FileNotFoundError:
                pass
            except PermissionError:
                pass

            if root_dir is None:
                try:
                    if os.path.exists(monorepo_root_dir):
                        # Monorepo directory is searched next
                        if any(os.path.exists(os.path.join(monorepo_root_dir, x)) for x in settings_filenames):
                            root_dir = monorepo_root_dir
                            root_offset = 0
                # Handle the possibility that directory access is prohibited
                except FileNotFoundError:
                    pass
                except PermissionError:
                    pass

            # Error if still not found
            if root_dir is None:
                raise RuntimeError(f"Settings files .env, settings.yaml, or both must be present "
                                   f"in either superproject or monorepo root."
                                   f"""Expected layout:
+ Superproject root
    ++ (settings files)
    ++ component_1
        --- (settings files here will be ignored for superproject layout)
        +++ (files for component_1)
    ++ component_2
        --- (settings files here will be ignored for superproject layout)
        +++ (files for component_2)     
OR
+ Monorepo root
    ++ (settings files)
    ++ (files for component_1)
    ++ (files for component_2)
Directories searched in the order of priority:
- Superproject root: {superproject_root_dir}
- Monorepo root: {monorepo_root_dir}
""")
            obj = ProjectSettings(
                root_dir=root_dir,
                root_offset=root_offset
            )
            cls.__instance = obj
        return cls.__instance
