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
from dataclasses import dataclass
from typing import List
from cl.runtime.configs.config import Config
from cl.runtime.configs.config_key import ConfigKey
from cl.runtime.context.context import Context
from cl.runtime.file.csv_file_reader import CsvFileReader
from cl.runtime.settings.settings import Settings


@dataclass(slots=True, kw_only=True)
class PreloadSettings(Settings):
    """Settings for preloading records from files."""

    dirs: List[str] | None = None
    """
    Absolute or relative (to Dynaconf project root) directory paths under which preloaded data is located.
    
    Notes:
        - Each element of 'dir_path' will be searched for csv, yaml, and json subdirectories
        - For CSV, the data is in csv/.../ClassName.csv where ... is optional dataset
        - For YAML, the data is in yaml/ClassName/.../KeyToken1;KeyToken2.yaml where ... is optional dataset
        - For JSON, the data is in json/ClassName/.../KeyToken1;KeyToken2.json where ... is optional dataset
    """

    configs: List[str] | None = None
    """Method Config.run_configure will run for each specified config_id (the record must exist in preloads)."""

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""

        # Convert to absolute paths if specified as relative paths and convert to list if single value is specified
        self.dirs = self.normalize_paths("dirs", self.dirs)

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_preload"

    def preload(self) -> None:
        """Preload from the specified directory paths."""

        # Get current context
        context = Context.current()

        # Process CSV preloads
        csv_files = self._get_files("csv")
        [CsvFileReader(file_path=csv_file).read() for csv_file in csv_files]

    def configure(self) -> None:
        """Execute configure for each config_id specified in PreloadSettings.configs."""
        if self.configs is not None and len(self.configs) > 0:

            # Load configs
            config_keys = [ConfigKey(config_id=config_id) for config_id in self.configs]
            config_records = list(Context.current().load_many(Config, config_keys))

            # Error message if a config is not found # TODO: Move to database allow_missing_record is implemented
            if any(config_record is None for config_record in config_records):
                keys_without_records = [key for key, record in zip(config_keys, config_records) if record is None]
                keys_without_records_str = "\n".join(f"  - {key.config_id}" for key in keys_without_records)
                preload_dirs_str = "\n".join(f"  - {os.path.normpath(x)}" for x in self.dirs)
                raise RuntimeError(
                    f"Preload directories in in 'PreloadSettings.configs' do not have config records "
                    f"for the following config_id specified in 'PreloadSettings.configs'.\n"
                    f"Missing config records:\n{keys_without_records_str}\n"
                    f"Preload directories searched (in priority order):\n{preload_dirs_str}"
                )

            # Run configure for the specified records
            tuple(config_record.run_configure() for config_record in config_records)

    def _get_files(self, ext: str) -> List[str]:
        # Return empty list if no dirs are specified in settings
        if self.dirs is None or len(self.dirs) == 0:
            return []

        # Normalize dirs to remove redundant slash at the end
        dirs = [os.path.normpath(x) for x in self.dirs]

        # Add dot prefix from ext if not included
        ext = f".{ext}" if not ext.startswith(".") else ext

        # Walk through the directory tree for each specified preload dir
        result = []
        for preload_dir in dirs:
            for dir_path, dir_names, filenames in os.walk(preload_dir):

                dir_name = os.path.basename(dir_path)
                if not dir_name.startswith("."):
                    # Add files with extension ext except from a dot-prefixed directory
                    result.extend(os.path.normpath(os.path.join(dir_path, f)) for f in filenames if f.endswith(ext))

                # Modify list in place to exclude dot-prefixed directories
                dir_names[:] = [d for d in dir_names if not d.startswith(".")]
        return result
