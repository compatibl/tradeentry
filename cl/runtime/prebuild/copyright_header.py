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
from fnmatch import fnmatch


def check_copyright_header(
        root_paths: Iterable[str | Path],
        *,
        copyright_header: str | None = None,
        include_patterns: List[str] | None = None,
        exclude_patterns: List[str] | None = None
) -> List[str] | None:
    """
    Check that the specified copyright header is present in all files with the specified glob filename pattern.

    Returns:
        List of absolute paths or None if all files are present.

    Args:
        root_paths: List of root directories under which files matching the pattern will be checked
        copyright_header: Optional copyright header, defaults to project contributors Apache header
        include_patterns: Optional list of filename glob patterns to include, use the defaults in code if not specified
        exclude_patterns: Optional list of filename glob patterns to exclude, use the defaults in code if not specified
    """

    # Use the project contributors Apache header if not specified by the caller
    if copyright_header is None:
        copyright_header = """# Copyright (C) 2023-present The Project Contributors
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
"""

    # Use default include patterns if not specified by the caller
    if include_patterns is None:
        include_patterns = ["*.py"]

    # Use default exclude patterns if not specified by the caller
    if exclude_patterns is None:
        exclude_patterns = ["__init__.py"]

    result = []

    # Apply to each element of root_paths
    for root_path in root_paths:

        # Convert to path if provided in string format
        if isinstance(root_path, str):
            root_path = Path(root_path)

        # Walk the directory tree
        for dir_path, dir_names, filenames in os.walk(root_path):

            # Apply exclude patterns
            filenames = [x for x in filenames if not any(fnmatch(x, y) for y in exclude_patterns)]

            # Apply include patterns
            filenames = [x for x in filenames if any(fnmatch(x, y) for y in include_patterns)]

            for filename in filenames:

                # Load the file
                file_path = os.path.join(dir_path, filename)
                with open(file_path, 'r') as file:
                    file_header = file.read(len(copyright_header))
                    if file_header != copyright_header:
                        result.append(str(file_path))

    # List of files with copyright header error or None if all files are present
    if len(result) > 0:
        return result
    else:
        return None
