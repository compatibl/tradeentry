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

from cl.runtime.prebuild.copyright_header import check_copyright_header

# Check copyright headers and fix missing trailing blank line
# All other copyright header errors cause an exception
if __name__ == '__main__':

    # Project root assuming the script is located in project_root/scripts
    project_path = Path(__file__).parent.parent

    # Relative source root paths
    relative_paths = ["cl", "stubs", "tests"]

    # Absolute source root paths
    root_paths = [project_path / x for x in relative_paths]

    # Create __init__.py files in subdirectories under each element of source_paths
    files_with_copyright_header_error, files_with_trailing_line_error = check_copyright_header(root_paths, fix_trailing_blank_line=True)

    if files_with_copyright_header_error:
        raise RuntimeError("Invalid copyright header in file(s):\n" +
              "".join([f"    {file}\n" for file in files_with_copyright_header_error]))
    elif files_with_trailing_line_error:
        print("Adding a missing blank line after copyright header in file(s):\n" +
              "".join([f"    {file}\n" for file in files_with_trailing_line_error]))
    else:
        print("Verified copyright header and trailing blank line under directory root(s):\n" +
              "".join([f"    {root_path}\n" for root_path in root_paths]))
