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


def add_init_files(root_path):
    """
    Go through every directory under the specified root directory and add an empty __init__.py
    if the directory already has .py files but not yet __init__.py.
    """

    # Walk the directory tree
    for dir_path, dir_names, filenames in os.walk(root_path):

        # Check if there are .py files in the directory
        if any(filename.endswith('.py') for filename in filenames):

            # Check if __init__.py is missing
            init_file = os.path.join(dir_path, '__init__.py')
            if not os.path.exists(init_file):

                # Create an empty __init__.py file if it is missing but other .py files are present
                with open(init_file, 'w') as f:
                    pass
                print(f"Created {init_file}")


if __name__ == '__main__':

    # Project root assuming the script is located in project_root/scripts
    project_path = Path(__file__).parent.parent

    # Relative source root paths
    relative_paths = ["cl", "stubs"]

    # Absolute source root paths
    root_paths = [project_path / x for x in relative_paths]

    # Create __init__.py files in subdirectories under each element of source_paths
    [add_init_files(root_path) for root_path in root_paths]


