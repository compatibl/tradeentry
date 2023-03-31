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
from typing import Any, Dict

from cl.runtime.storage.cl_record import ClRecord


@dataclass
class ClDataClassRecord(ClRecord, ABC):
    """
    Base class for polymorphic records where all serializable
    data is stored in dataclass fields.

    The recommended inheritance chain includes two classes:

    rt.DataClassRecord > SampleRecordKey > SampleRecord > DerivedRecord

    * SampleRecordKey contains primary key attributes. It can be used
      as a foreign key attribute in other data classes, providing
      static (code inspection-based) type safety.
    * SampleRecord is derived from SampleRecordKey and contains all
      attributes except those included in SampleRecordKey class.

    If a separate key class is not required, a simpler inheritance
    chain can be used:

    rt.DataClassRecord > SampleRecord > DerivedRecord

    With this simpler inheritance chain, foreign key can be stored in
    other data types with runtime type safety as the string generated
    by to_pk() method.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize self as dictionary.

        Default implementation uses runtime class introspection.
        Derived classes may override for greater performance.
        """
        raise NotImplementedError()  # TODO: currently a stub
        return {}

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Populate self from dictionary.

        Default implementation uses runtime class introspection.
        Derived classes may override for greater performance.
        """
        raise NotImplementedError()  # TODO: currently a stub
        pass
