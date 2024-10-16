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
from cl.runtime.settings.context_settings import ContextSettings


class ImportUtil:
    """Helper methods for working with imports."""

    @classmethod
    def check_imports(cls) -> None:
        """Check that all imports succeed, output a detailed error message otherwise."""
        # Get the list of packages
        context_packages = ContextSettings.instance().packages
        all_packages = []
        for package in context_packages:
            if package.startswith("stubs.") or package.startswith("tests."):
                all_packages.append(package)
            else:
                # TODO: Also support tests
                all_packages.extend([package, f"stubs.{package}"])

        # Find import errors in each package
        import_errors = [item for sublist in map(cls._check_package, all_packages) for item in sublist]

        # Report errors
        if import_errors:
            # TODO: Improve formatting of the report
            import_errors_str = "\n".join(import_errors)
            raise RuntimeError(f"Import errors occurred on launch:\n{import_errors_str}\n")

    @classmethod
    def _check_package(cls, package_root: str) -> List[str]:
        """Check package for import errors."""
        errors: List[str] = []
        try:
            package_import = __import__(package_root)
        except ImportError as error:
            raise Exception(f"Cannot import module: {error.name}. Check sys.path")

        packages = list(pkgutil.walk_packages(path=package_import.__path__, prefix=package_import.__name__ + "."))
        modules = [x for x in packages if not x.ispkg]
        for m in modules:
            try:
                package_import = importlib.import_module(m.name)
            except SyntaxError as error:
                errors.append(
                    f"Cannot import module: {m.name}. Error: {error.msg}. Line: {error.lineno}, {error.offset}")
                continue
            except Exception as error:
                errors.append(f"Cannot import module: {m.name}. Error: {error.args}")

        return errors
