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

from __future__ import annotations
import importlib
import inspect
from pkgutil import walk_packages
from types import ModuleType
from typing import List
from inflection import titleize
from pydantic import BaseModel
from cl.runtime.primitive.string_util import to_pascal_case


def is_record(cls):
    """Return true if the type is a record based on the presence of 'get_key' method."""
    return inspect.isclass(cls) and hasattr(cls, 'get_key') and callable(getattr(cls, 'get_key'))


class TypeResponse(BaseModel):
    """REST API response for a single item of the list returned by the /data/types route."""

    name: str
    """Class name (may be customized in settings)."""

    module: str
    """Module path in dot-delimited format (may be customized in settings)."""

    label: str
    """Type label displayed in the UI is humanized class name (may be customized in settings)."""

    class Config:
        alias_generator = to_pascal_case
        populate_by_name = True

    @staticmethod
    def get_modules(packages: List[str]) -> List[ModuleType]:
        """
        Get a list of ModuleType objects for submodules at all levels of the specified packages or root modules.
        Args:
            packages: List of packages or root module strings in dot-delimited format, for example ['cl.runtime']
        """
        result = []
        for package in packages:
            # Import root module of the package
            root_module = importlib.import_module(package)
            result.append(root_module)  # Add the root module itself
            # Get module info for all submodules, note the trailing period added as per walk_packages documentation
            for module_info in walk_packages(root_module.__path__, root_module.__name__ + "."):
                module_name = module_info.name
                # Import the submodule using its full name
                submodule = importlib.import_module(module_name)
                result.append(submodule)
        return result

    @staticmethod
    def get_types() -> List[TypeResponse]:
        """Implements /schema/types route."""

        packages = ["cl.runtime"]

        result = []
        modules = TypeResponse.get_modules(packages)
        record_types = [
            record_type
            for module in modules
            for name, record_type in inspect.getmembers(module, is_record)
        ]
        for record_type in record_types:
            type_response = TypeResponse(
                name=record_type.__name__,
                module=to_pascal_case(record_type.__module__),
                label=titleize(record_type.__name__),
            )
            result.append(type_response)
        return result
