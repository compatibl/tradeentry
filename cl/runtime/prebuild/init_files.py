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
from typing import List
from cl.runtime.settings.context_settings import ContextSettings
from cl.runtime.settings.project_settings import ProjectSettings


def check_init_files(
    *,
    source_dirs: List[str] | None = None,
    apply_fix: bool,
    verbose: bool = False,
) -> None:
    """
    Check that __init__.py is present in all subdirectories of 'root_path'.
    Optionally create when missing.

    Args:
        source_dirs: Directories under which files will be checked
        apply_fix: If True, create an empty __init__.py file when missing
        verbose: Print messages about fixes to stdout if specified
    """

    # The list of packages from context settings
    packages = ContextSettings.instance().packages

    missing_files = []
    all_root_paths = set()
    for package in packages:
        # Add paths to source and stubs directories
        if (x := ProjectSettings.get_source_root(package)) is not None and x not in all_root_paths:
            all_root_paths.add(x)
        if (x := ProjectSettings.get_stubs_root(package)) is not None and x not in all_root_paths:
            all_root_paths.add(x)

    # Apply to each element of root_paths
    for root_path in all_root_paths:
        # Walk the directory tree
        for dir_path, dir_names, filenames in os.walk(root_path):
            # Check for .py files in the directory
            # This will not check if there are .py files in subdirectories
            # to avoid adding __init__.py files to namespace package root
            if any(filename.endswith(".py") for filename in filenames):
                # Check if __init__.py is missing
                init_file_path = os.path.join(dir_path, "__init__.py")
                if not os.path.exists(init_file_path):
                    missing_files.append(str(init_file_path))
                    if apply_fix:
                        # Create an empty __init__.py file if it is missing but other .py files are present
                        with open(init_file_path, "w") as f:
                            pass

    if missing_files:
        missing_files_msg = "__init__.py file(s):\n" + "".join(
            [f"    {missing_file}\n" for missing_file in missing_files]
        )
        if not apply_fix:
            raise RuntimeError(f"Found missing {missing_files_msg}")
        elif verbose:
            print(f"Created {missing_files_msg}")
    elif verbose:
        print(
            "Verified that all __init__.py files are present under directory root(s):\n"
            + "".join([f"    {root_path}\n" for root_path in sorted(all_root_paths)])
        )
