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

import importlib
import pkgutil
from typing import List
import pytest


def _check_package(package_root: str) -> List[str]:  # TODO: Move this method to cl.runtime.testing module
    """Check package for import errors."""
    errors: List[str] = []
    try:
        package_import = __import__(package_root)
    except ImportError as error:
        raise Exception(f'Cannot import module: {error.name}. Check sys.path')

    packages = list(pkgutil.walk_packages(path=package_import.__path__, prefix=package_import.__name__ + '.'))
    modules = [x for x in packages if not x.ispkg]
    for m in modules:
        try:
            package_import = importlib.import_module(m.name)

            # TODO: Validate type hints
            # data_classes = inspect.getmembers(package_import, attrs.has)
            # [ClassInfo.get_type_hints(x[1]) for x in data_classes]
        except SyntaxError as error:
            errors.append(f'Cannot import module: {m.name}. Error: {error.msg}. Line: {error.lineno}, {error.offset}')
            continue
        except Exception as error:
            errors.append(f'Cannot import module: {m.name}. Error: {error.args}')

    return errors


def test_import():
    errors = _check_package("cl.runtime")
    if errors:
        print('\n'.join(errors))
    assert 0 == len(errors)


if __name__ == '__main__':
    pytest.main([__file__])
