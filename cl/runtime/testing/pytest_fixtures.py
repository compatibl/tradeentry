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
import pytest

from cl.runtime.settings.log_settings import LogSettings


def get_caller_name(*, caller_file: str) -> str:  # TODO: Use __name__ instead, review use
    """
    Get caller script name without extension from its __file__ variable.

    Use to make test input and output files begin from the prefix
    based on test .py file name.
    """

    file_path, file_name_with_ext = os.path.split(caller_file)
    file_name, file_ext = os.path.splitext(file_name_with_ext)
    return file_name


@pytest.fixture(scope="session", autouse=True)
def log_fixture(request):
    """Pytest session fixture to set log file prefix for test execution."""

    # Set log file prefix
    log_settings = LogSettings.instance()
    log_settings.filename_prefix = "tests"


@pytest.fixture(scope="module", autouse=True)
def local_dir_fixture(request):
    """Pytest module fixture to make test module directory the local directory during test execution."""

    # Change test working directory to the directory of test source
    # so output files are placed next to the test module
    os.chdir(request.fspath.dirname)

    # Back to the test
    yield

    # Change directory back before exiting the text
    os.chdir(request.config.invocation_dir)
