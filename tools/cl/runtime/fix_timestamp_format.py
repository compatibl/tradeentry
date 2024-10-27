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
import re


def update_text(text: str) -> str:
    """Update Timestamp format in text."""
    # Pattern for the legacy format
    legacy_pattern = r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{3})Z-([a-fA-F0-9]{20})"
    # Replace delimiters to match new format
    new_format = r"\1-\2-\3-\4-\5-\6-\7-\8"

    # Perform the substitution
    updated_text = re.sub(legacy_pattern, new_format, text)
    return updated_text


def update_file(file_path: str):
    """Update Timestamp format in file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace the target string with the replacement
    content = update_text(content)

    # Write back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def update_dir(dir_path: str):
    """Update Timestamp format in text in all directories under the specified root."""
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".completions.csv"):
                file_path = os.path.join(root, file)
                update_file(file_path)
                print(f"Timestamp format updated in: {file_path}")


if __name__ == '__main__':

    # Replace by the desired root
    root_dir = None

    if root_dir is None:
        raise RuntimeError("Specify root directory for Timestamp format update.")

    # Update Timestamp format in text in all directories under the specified root.
    update_dir(root_dir)  # noqa
