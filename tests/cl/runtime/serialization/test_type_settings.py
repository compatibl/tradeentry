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

import pytest
from cl.runtime.serialization.type_settings import TypeSettings
from stubs.cl.runtime import StubDataclassDerivedRecord
from stubs.cl.runtime import StubDataclassRecord
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_aliased_record import StubDataclassAliasedRecord


@pytest.mark.skip("Aliases are not yet supported.")
def test_type_alias():
    """Test type alias methods."""

    TypeSettings.set_type_alias(StubDataclassDerivedRecord, "StubDataclassRenamedRecord")

    assert TypeSettings.get_type_alias(StubDataclassRecord) == "StubDataclassRecord"  # Alias is not set
    assert TypeSettings.get_type_alias(StubDataclassDerivedRecord) == "StubDataclassRenamedRecord"  # Alias set in test
    assert (
        TypeSettings.get_type_alias(StubDataclassAliasedRecord) == "StubDataclassAliasedRecordNewName"
    )  # Alias set in class


if __name__ == "__main__":
    pytest.main([__file__])
