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
from typing import ClassVar, Literal, cast
from typing_extensions import Self
from cl.runtime.records.dataclasses_extensions import missing

SETTINGS_FILES_ENVVAR = "CL_SETTINGS_FILES"
"""The name of environment variable used to override the settings file(s) names or locations."""


@dataclass(slots=True, kw_only=True)
class ProjectSettings:
    """
    Information about the project location and layout used to search for settings and packages.
    This class finds the location of .env or settings.yaml and detects one of two supported layouts:

    One-level (suitable only for monorepo git layout):
        - project and packages root (one level layout)
            -- project files
            -- package files (files from all packages are interleaved under a common root)

    Two-level (suitable for monorepo, submodules or subtree git layout):
        - project root (first level of two-level layout)
            -- project files
            -- package root (second level of two-level layout)
                --- package files (files from each package are under a separate package root)
    """

    project_root: str = missing()
    """Project root directory is the location of .env or settings.yaml file."""

    project_levels: int = missing()
    """Number of levels in project layout (one or two)."""

    __instance: ClassVar[ProjectSettings] = None
    """Singleton instance."""

    def __post_init__(self):
        """Perform validation and type conversions."""
        if self.project_levels != 1 and self.project_levels != 2:
            raise RuntimeError(f"Field 'ProjectSettings.project_levels' must be 1 or 2.")

    @classmethod
    def get_project_root(cls) -> str:
        """Project root directory is the location of .env or settings.yaml file."""
        return cls.instance().project_root

    @classmethod
    def get_source_root(cls, package: str) -> str:
        """Source code root (the entry in PYTHONPATH) for dot-delimited package, e.g. 'stubs.cl.runtime'."""
        project_root = cls.instance().project_root
        project_levels = cls.instance().project_levels
        relative_path = package.replace(".", os.sep)
        if project_levels == 1:
            # One-level project, search directly under project root
            search_paths = [os.path.normpath(os.path.join(project_root, relative_path, "__init__.py"))]
        elif project_levels == 2:
            # Two-level project, check each dot-delimited package token in reverse order as potential package root
            package_tokens = package.split(".")
            package_tokens.reverse()
            search_paths = [
                os.path.normpath(os.path.join(project_root, x, relative_path, "__init__.py"))
                for x in package_tokens
            ]
        else:
            raise RuntimeError(f"Field 'ProjectSettings.project_levels' must be 1 or 2.")

        # Find the first directory with __init__.py
        init_path = next((x for x in search_paths if os.path.exists(x)), None)
        if init_path is not None:
            result = os.path.normpath(os.path.dirname(init_path))
            return result
        else:
            search_paths_str = "\n".join(search_paths)
            raise RuntimeError(f"Did not find  __init__.py for package '{package}'. Location searched:\n"
                               f"{search_paths_str}\n")

    @classmethod
    def get_wwwroot_dir(cls) -> str:
        """Class method returning path to wwwroot directory under project root directory."""
        project_root = cls.get_project_root()
        return os.path.normpath(os.path.join(project_root, "wwwroot"))

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

            project_root = None
            project_levels = None
            try:
                if os.path.exists(superproject_root_dir):
                    # Supermodule directory takes priority but only if it contains one of the settings files
                    if any(os.path.exists(os.path.join(superproject_root_dir, x)) for x in settings_filenames):
                        project_root = superproject_root_dir
                        project_levels = 2
            # Handle the possibility that directory access is prohibited
            except FileNotFoundError:
                pass
            except PermissionError:
                pass

            if project_root is None:
                try:
                    if os.path.exists(monorepo_root_dir):
                        # Monorepo directory is searched next
                        if any(os.path.exists(os.path.join(monorepo_root_dir, x)) for x in settings_filenames):
                            project_root = monorepo_root_dir
                            project_levels = 1
                # Handle the possibility that directory access is prohibited
                except FileNotFoundError:
                    pass
                except PermissionError:
                    pass

            # Error if still not found
            if project_root is None:
                raise RuntimeError(
                    f"""Project settings ('.env' or 'settings.yaml' files) could not be found. Locations searched:
1. {superproject_root_dir}
2. {monorepo_root_dir}
"""
                )
            obj = ProjectSettings(project_root=project_root, project_levels=project_levels)
            cls.__instance = obj
        return cls.__instance
