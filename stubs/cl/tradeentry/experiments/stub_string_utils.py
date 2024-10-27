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

import re
from typing import Optional

# TODO: Convert to helper class methods


def extract_between_backticks(text: str) -> Optional[str]:

    pattern = r"```(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    if not matches:
        return None

    return matches[0]


def normalize_string(string: str) -> str:  # TODO: Move to StringUtil or another helper class
    """
    Removes newlines and extra spaces from a string.
    """
    return "".join(string.replace("\n", "").split())
