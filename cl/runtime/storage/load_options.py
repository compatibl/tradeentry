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

from cl.runtime.storage.attrs_data_util import attrs_data
from cl.runtime.storage.attrs import attrs_field, attrs_class
from cl.runtime.storage.data import Data


@attrs_data
class LoadOptions(Data):
    """Optional flags for load methods."""

    none_if_not_found: bool = attrs_field()
    """Return None instead of error message if the record is not found."""

    none_if_no_key: bool = attrs_field()
    """
    Return None instead of error message if key=None is passed as argument.

    This option can be used to simplify the code for loading a record
    from a key stored in an optional element.
    """
