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

from cl.runtime.prebuild.copyright_header import check_copyright_headers

# Check copyright headers and fix missing trailing blank line
# All other copyright header errors cause an exception
if __name__ == '__main__':
    # Create __init__.py files in subdirectories under each element of source_paths
    check_copyright_headers(fix_trailing_blank_line=True, verbose=True)