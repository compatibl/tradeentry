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
from cl.runtime.prebuild.init_files import check_init_files

if __name__ == '__main__':

    # Project root assuming the script is located in project_root/scripts
    project_path = Path(__file__).parent.parent

    # Relative source root paths
    relative_paths = ["cl", "stubs"]

    # Absolute source root paths
    root_paths = [project_path / x for x in relative_paths]

    # Create __init__.py files in subdirectories under each element of source_paths
    missing_files = check_init_files(root_paths, apply_fix=True)

    if missing_files:
        print("Adding missing __init__.py file(s):\n" +
              "".join([f"    {missing_file}\n" for missing_file in missing_files]))
    else:
        print("Verified that all __init__.py files are present under directory root(s):\n" +
              "".join([f"    {root_path}\n" for root_path in root_paths]))
