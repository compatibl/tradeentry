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
from stubs.cl.runtime import StubAttrsDerivedRecord
from stubs.cl.runtime import StubAttrsRecord
from stubs.cl.runtime.classes.attrs.stub_attrs_aliased_record import StubAttrsAliasedRecord


@pytest.mark.skip("Aliases are not yet supported.")
def test_type_alias():
    """Test type alias methods."""

    TypeSettings.set_type_alias(StubAttrsDerivedRecord, "StubAttrsRenamedRecord")

    assert TypeSettings.get_type_alias(StubAttrsRecord) == "StubAttrsRecord"  # Alias is not set
    assert TypeSettings.get_type_alias(StubAttrsDerivedRecord) == "StubAttrsRenamedRecord"  # Alias set in test
    assert TypeSettings.get_type_alias(StubAttrsAliasedRecord) == "StubAttrsAliasedRecordNewName"  # Alias set in class


if __name__ == "__main__":
    pytest.main([__file__])
