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

from dataclasses import dataclass
from cl.runtime.configs.config import Config
from cl.runtime.context.context import Context
from cl.runtime.plots.group_bar_plot import GroupBarPlot
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
from stubs.cl.runtime import StubHandlers
from stubs.cl.runtime import StubPlots
from stubs.cl.runtime import StubViewers
from stubs.cl.runtime import StubInstanceViewers


@dataclass(slots=True, kw_only=True)
class StubRuntimeConfig(Config):
    """Save stub records to storage."""

    def run_configure(self) -> None:
        """Populate the current or default database with stub records."""

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
        stub_viewers_data_records = [StubInstanceViewers(stub_id=f"N{i}") for i in range(10)]
        stub_plots = [StubPlots(stub_id=f"O{i}") for i in range(10)]

        stub_dataclass_singleton_record = [StubDataclassSingleton()]

        all_records = [
            *stub_dataclass_records,
            *stub_dataclass_nested_fields,
            *stub_dataclass_derived_records,
            *stub_dataclass_derived_from_derived_records,
            *stub_dataclass_other_derived_records,
            *stub_dataclass_optional_fields_records,
            # TODO: Restore after supporting dt.date and dt.time for Mongo: *stub_dataclass_list_fields_records,
            # TODO: Restore after supporting dt.date and dt.time for Mongo: *stub_dataclass_dict_fields_records,
            # TODO: Restore after supporting dt.date and dt.time for Mongo: *stub_dataclass_dict_list_fields_records,
            # TODO: Restore after supporting dt.date and dt.time for Mongo: *stub_dataclass_list_dict_fields_records,
            # TODO: Restore after supporting dt.date and dt.time for Mongo: *stub_dataclass_primitive_fields_records,
            *stub_dataclass_singleton_record,
            *stub_viewers_records,
            *stub_handlers_records,
            *stub_viewers_data_records,
            *stub_plots,
        ]

        # save stubs to db
        Context.current().save_many(all_records)

    def run_configure_plots(self) -> None:
        """Configure plots."""

        bar_plot = GroupBarPlot()
        bar_plot.group_labels = ["Single Group"] * 2
        bar_plot.bar_labels = ["Bar 1", "Bar 2"]
        bar_plot.values = [85.5, 92]
        Context.current().save_one(bar_plot)
