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

SETTINGS_FILES_ENVVAR = "CL_SETTINGS_FILES"
"""The name of environment variable used to override the settings file(s) names or locations."""


@dataclass(slots=True, kw_only=True)
class ProjectSettings:
    """
    Information about the project location and layout (used to search for settings and submodules).

    Notes:
        - This class is used to search for .env or settings.yaml
        - It does not read data .env or settings.yaml because its initialization happens before
    """

    project_root: str = missing()
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

    component_offset: int = missing()
    """Directory levels between project root and component root (superproject=1, monorepo=0)."""

    __instance: ClassVar[ProjectSettings] = None
    """Singleton instance."""

    @classmethod
    def get_project_root(cls) -> str:
        """Class method returning project root directory."""
        return cls.instance().project_root

    @classmethod
    def get_component_offset(cls) -> int:
        """Directory levels between project root and component root (superproject=1, monorepo=0)."""
        return cls.instance().component_offset

    @classmethod
    def get_wwwroot_dir(cls) -> str:
        """Class method returning path to wwwroot directory under project root directory."""
        return os.path.normpath(os.path.join(cls.instance().project_root, "wwwroot"))

    @classmethod
    def get_databases_dir(cls) -> str:
        """Class method returning path to databases directory under project root directory."""
        project_root = cls.get_project_root()
        db_dir = os.path.join(project_root, "databases")
        if not os.path.exists(db_dir):
            # Create the directory if does not exist
            os.makedirs(db_dir)
        return db_dir

    @classmethod
    def instance(cls) -> Self:
        """Return singleton instance."""
        # Check if cached value exists, load if not found
        if cls.__instance is None:
            env_settings_files = os.getenv(SETTINGS_FILES_ENVVAR)
            if env_settings_files:
                # TODO: Handle by replacing settings.yaml in search by the specified list
                raise RuntimeError(
                    f"Override of the Dynaconf settings file(s) names or locations using envvar "
                    f"'{SETTINGS_FILES_ENVVAR}' is not supported in this version."
                )

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
                raise RuntimeError(
                    f"Settings files .env, settings.yaml, or both must be present "
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
"""
                )
            obj = ProjectSettings(project_root=root_dir, component_offset=root_offset)
            cls.__instance = obj
        return cls.__instance
