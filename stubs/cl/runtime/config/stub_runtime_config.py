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

from cl.runtime.backend.core.ui_app_state import UiAppState
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.config.config import Config
from cl.runtime.context.context import current_or_default_data_source
from dataclasses import dataclass
from stubs.cl.runtime import StubDataclassDerivedFromDerivedRecord
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassDictFields
from stubs.cl.runtime import StubDataclassDictListFields
from stubs.cl.runtime import StubDataclassListDictFields
from stubs.cl.runtime import StubDataclassListFields
from stubs.cl.runtime import StubDataclassNestedFields
from stubs.cl.runtime import StubDataclassOptionalFields
from stubs.cl.runtime import StubDataclassOtherDerivedRecord
from stubs.cl.runtime import StubDataclassPrimitiveFields
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime import StubDataclassSingleton
from stubs.cl.runtime.decorators.stub_handlers import StubHandlers
from stubs.cl.runtime.decorators.stub_viewers import StubViewers


@dataclass(slots=True, kw_only=True)
class StubRuntimeConfig(Config):
    """Save stub records to storage."""

    def configure(self) -> None:
        """Populate the current or default data source with stub records."""

        # Get current or default data source based on settings
        data_source = current_or_default_data_source()

        # Save self
        data_source.save_one(self)

        # Save UiAppState instance
        data_source.save_one(UiAppState(user=UserKey(username="root")))

        # Create stub instances
        stub_dataclass_records = [StubDataclassRecord(id=f"A{i}") for i in range(10)]
        stub_dataclass_nested_fields = [StubDataclassNestedFields(primitive=f"B{i}") for i in range(10)]
        stub_dataclass_derived_records = [StubDataclassDerivedRecord(id=f"C{i}") for i in range(10)]
        stub_dataclass_derived_from_derived_records = [
            StubDataclassDerivedFromDerivedRecord(id=f"D{i}") for i in range(10)
        ]
        stub_dataclass_other_derived_records = [StubDataclassOtherDerivedRecord(id=f"E{i}") for i in range(10)]
        stub_dataclass_list_fields_records = [StubDataclassListFields(id=f"F{i}") for i in range(10)]
        stub_dataclass_optional_fields_records = [StubDataclassOptionalFields(id=f"G{i}") for i in range(10)]
        stub_dataclass_dict_fields_records = [StubDataclassDictFields(id=f"H{i}") for i in range(10)]
        stub_dataclass_dict_list_fields_records = [StubDataclassDictListFields(id=f"I{i}") for i in range(10)]
        stub_dataclass_list_dict_fields_records = [StubDataclassListDictFields(id=f"J{i}") for i in range(10)]
        stub_dataclass_primitive_fields_records = [
            StubDataclassPrimitiveFields(key_str_field=f"K{i}") for i in range(10)
        ]

        stub_viewers_records = [StubViewers(stub_id=f"L{i}") for i in range(10)]
        stub_handlers_records = [StubHandlers(stub_id=f"M{i}") for i in range(10)]

        stub_dataclass_singleton_record = [StubDataclassSingleton()]

        all_records = [
            *stub_dataclass_records,
            *stub_dataclass_nested_fields,
            *stub_dataclass_derived_records,
            *stub_dataclass_derived_from_derived_records,
            *stub_dataclass_other_derived_records,
            *stub_dataclass_list_fields_records,
            *stub_dataclass_optional_fields_records,
            *stub_dataclass_dict_fields_records,
            *stub_dataclass_dict_list_fields_records,
            *stub_dataclass_list_dict_fields_records,
            *stub_dataclass_primitive_fields_records,
            *stub_dataclass_singleton_record,
            *stub_viewers_records,
            *stub_handlers_records,
        ]

        # save stubs to db
        data_source.save_many(all_records)
