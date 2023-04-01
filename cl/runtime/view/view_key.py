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

import cl.runtime as rt
from dataclasses import dataclass


@dataclass
class ViewKey(rt.ClassRecord):
    """
    The data shown alongside the record in the front end.

    When the record is displayed, the user interface backend
    will run a query for the view_for field where the value
    is primary key of the record for which the view is specified,
    and will display each View returned by the query on a separate
    tab or panel next to the record itself.
    """

    view_for: str = rt.class_field()
    """Primary key of the record for which the view is specified."""

    view_name: str = rt.class_field()
    """Name of the view displayed in the front end."""

    def to_pk(self) -> str:
        """Return primary key (PK) as string."""

        # Use composite_pk(...) method because one of the tokens is an embedded key
        return rt.RecordUtil.composite_pk('rt.View', self.view_for, self.view_name)
