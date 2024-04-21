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

from abc import ABC
from dataclasses import dataclass
from typing import Tuple, Type

from cl.runtime.classes.dataclasses.dataclass_fields import data_field
from cl.runtime.classes.dataclasses.dataclass_mixin import DataclassMixin

ViewKey = Tuple[Type['View'], Tuple[Type, ...], str]


@dataclass
class View(DataclassMixin, ABC):
    """
    The data shown alongside the record in the front end.

    When the record is displayed, the user interface backend
    will run a query for the view_for field where the value
    is primary key of the record for which the view is specified,
    and will display each View returned by the query on a separate
    tab or panel next to the record itself.
    """

    view_for: Tuple[Type, ...] = data_field()
    """Primary key of the record for which the view is specified."""

    view_name: str = data_field()
    """Name of the view displayed in the front end."""

    def get_key(self) -> ViewKey:
        """Return primary key of this instance in semicolon-delimited string format."""
        return View, self.view_for, self.view_name

