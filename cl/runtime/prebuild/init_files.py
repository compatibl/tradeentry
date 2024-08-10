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
from typing import Iterable, List


def check_init_files(root_paths: Iterable[str | Path], *, apply_fix: bool) -> List[str] | None:
    """
    Check that __init__.py is present in all subdirectories of 'root_path'.
    Optionally create when missing.

    Returns:
        List of missing absolute paths or None if all files are present.
        The list is returned for information purposes even when apply_fix = True.

    Args:
        root_paths: List of root directories
        apply_fix: If True, create an empty __init__.py file when missing.
    """

    missing_files = []

    # Apply to each element of root_paths
    for root_path in root_paths:

        # Convert to path if provided in string format
        if isinstance(root_path, str):
            root_path = Path(root_path)

        # Walk the directory tree
        for dir_path, dir_names, filenames in os.walk(root_path):

            # Check if there are .py files in the directory
            if any(filename.endswith('.py') for filename in filenames):

                # Check if __init__.py is missing
                init_file_path = os.path.join(dir_path, '__init__.py')
                if not os.path.exists(init_file_path):
                    missing_files.append(str(init_file_path))
                    if apply_fix:
                        # Create an empty __init__.py file if it is missing but other .py files are present
                        with open(init_file_path, 'w') as f:
                            pass

    # List of missing absolute paths or None if all files are present
    if len(missing_files) > 0:
        return missing_files
    else:
        return None
