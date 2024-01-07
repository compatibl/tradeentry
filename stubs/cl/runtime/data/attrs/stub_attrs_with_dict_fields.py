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

import datetime as dt
from typing import Any, Dict, List, Optional
from cl.runtime.data.attrs.attrs_record_util import attrs_record
from cl.runtime.data.attrs.attrs_field_util import attrs_field
from cl.runtime.data.attrs.stubs.stub_attrs_base_record import StubAttrsBaseRecord
from cl.runtime.data.attrs.stubs.stub_attrs_derived_record import StubAttrsDerivedRecord
from cl.runtime.data.attrs.stubs.stub_attrs_with_dict_fields_key import StubAttrsWithDictFieldsKey


@attrs_record
class StubAttrsWithDictFields(StubAttrsWithDictFieldsKey):
    """Stub record whose elements are dictionaries."""

    dict_of_float: Optional[Dict[str, float]] = attrs_field()
    """Stub field."""

    dict_of_derived_samples: Optional[Dict[str, StubAttrsDerivedRecord]] = attrs_field()
    """Stub field."""

    dict_of_base_samples: Optional[Dict[str, StubAttrsBaseRecord]] = attrs_field()
    """Stub field."""

    dict_of_dates: Optional[Dict[str, dt.date]] = attrs_field()
    """Stub field."""

    dict_of_float_list: Optional[Dict[str, List[float]]] = attrs_field()
    """Stub field."""

    dict_of_base_sample_list: Optional[Dict[str, List[StubAttrsBaseRecord]]] = attrs_field()
    """Stub field."""

    dict_of_derived_sample_list: Optional[Dict[str, List[StubAttrsDerivedRecord]]] = attrs_field()
    """Stub field."""

    dict_of_dates_list: Optional[Dict[str, List[dt.date]]] = attrs_field()
    """Stub field."""
