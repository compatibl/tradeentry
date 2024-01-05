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
from cl.runtime.decorators.data_class_decorator import data_class
from cl.runtime.decorators.data_field_decorator import data_field
from cl.runtime.storage.record import Record


@data_class
class View(Record, ABC):
    """
    The data shown alongside the record in the front end.

    When the record is displayed, the user interface backend
    will run a query for the view_for field where the value
    is primary key of the record for which the view is specified,
    and will display each View returned by the query on a separate
    tab or panel next to the record itself.
    """

    view_for: str = data_field()
    """Primary key of the record for which the view is specified."""

    view_name: str = data_field()
    """Name of the view displayed in the front end."""

    @staticmethod
    def get_common_base():
        """Type of the common base for all classes stored in the same table as this class."""
        return View

    @staticmethod
    def create_key(view_for: str, view_name: str) -> str:
        """Create primary key from arguments in semicolon-delimited string format."""
        return f'{view_for};{view_name}'

    def get_key(self) -> str:
        """Return primary key of this instance in semicolon-delimited string format."""
        return f'{self.view_for};{self.view_name}'
