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

from pathlib import Path
from typing import List, Iterable

from cl.runtime.records.dataclasses_extensions import field

from cl.runtime.settings.settings import Settings, dotenv_dir_path, dynaconf_dir_path
from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class PreloadSettings(Settings):
    """Runtime settings for preloading records from files."""

    csv_dirs: List[str] = field(default_factory=lambda: "preload/csv")
    """CSV data directory as absolute or relative (to Dynaconf project root) path."""

    yaml_dirs: List[str] = field(default_factory=lambda: "preload/yaml")
    """YAML data directory as absolute or relative (to Dynaconf project root) path."""

    json_dirs: List[str] = field(default_factory=lambda: "preload/json")
    """JSON data directory as absolute or relative (to Dynaconf project root) path."""

    def __post_init__(self):
        """Perform validation and type conversions."""

        # Convert to absolute path if specified as relative path
        self.csv_dirs = self.normalize_paths("csv_dirs", self.csv_dirs)
        self.yaml_dirs = self.normalize_paths("yaml_dirs", self.yaml_dirs)
        self.json_dirs = self.normalize_paths("json_dirs", self.json_dirs)

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_preload"

    @classmethod
    def normalize_paths(cls, field_name: str, field_value: Iterable[str | Path] | str | Path) -> List[str]:
        """Convert to absolute path if path relative to the location of .env or Dynaconf file is specified."""
        
        # Check that the argument is either a string or a list of strings
        if isinstance(field_value, str) or isinstance(field_value, Path):
            paths = [field_value]
        elif hasattr(field_value, "__iter__"):
            paths = list(field_value)
        else:
            raise RuntimeError(f"Field '{field_name}' in class '{cls.__name__}' "
                               f"must be a string or Path variable or their iterable.")

        result = [cls.normalize_path(field_name, path) for path in paths]
        return result

    @classmethod
    def normalize_path(cls, field_name: str, field_value: Path | str) -> str:
        """Convert to absolute path if path relative to the location of .env or Dynaconf file is specified."""

        # Convert to Path if specified as string
        if isinstance(field_value, Path):
            path = field_value
        elif isinstance(field_value, str):
            path = Path(field_value)
        elif field_value is None or field_value == "":
            raise RuntimeError(f"Field '{field_name}' in class '{cls.__name__}' has an empty element.")
        else:
            raise RuntimeError(f"Field '{field_name}' in class '{cls.__name__}' has an element "
                               f"with type {type(field_value)} which is neither a Path nor a string.")

        if not path.is_absolute():
            if dotenv_dir_path is not None:
                # Use .env file location if found
                path = Path(dotenv_dir_path) / path
            elif dynaconf_dir_path is not None:
                # Use Dynaconf settings file location if found
                path = Path(dynaconf_dir_path) / path
            else:
                raise RuntimeError(f"Cannot resolve relative preload path value {path} for {field_name} when "
                                   "neither .env nor dynaconf settings file is present to use as project root.")

        # Return as absolute path string
        return str(path)
