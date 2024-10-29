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
from cl.runtime.db.protocols import TKey
from cl.runtime.records.record_util import RecordUtil
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.runtime import StubDataclassDerivedFromDerivedRecord, StubDataclassComposite
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


class _Base:
    """Test class."""

    def get_key(self) -> TKey:
        raise NotImplementedError()

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""
        RegressionGuard().write("> _Base.init")


class _Derived(_Base):
    """Test class."""

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""
        RegressionGuard().write(">> _Derived.init")


class _DerivedFromDerivedWithInit(_Derived):
    """Test class."""

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""
        RegressionGuard().write(">>> _DerivedFromDerivedWithInit.init")


class _DerivedFromDerivedWithoutInit(_Derived):
    """Test class."""


def test_init_all():
    """Test RecordUtil.init_all method."""

    guard = RegressionGuard()

    guard.write("Testing _Base:")
    RecordUtil.init_all(_Base())
    guard.write("Testing _Derived:")
    RecordUtil.init_all(_Derived())
    guard.write("Testing _DerivedFromDerivedWithInit:")
    RecordUtil.init_all(_DerivedFromDerivedWithInit())
    guard.write("Testing _DerivedFromDerivedWithoutInit:")
    RecordUtil.init_all(_DerivedFromDerivedWithoutInit())

    RegressionGuard.verify_all()


def test_is_instance():
    """Test RecordUtil.validate method."""

    # Primitive types
    assert RecordUtil._is_instance(True, bool)
    assert not RecordUtil._is_instance(None, bool)

    # Primitive types | None
    assert RecordUtil._is_instance(True, bool | None)
    assert RecordUtil._is_instance(None, bool | None)


def test_validate():
    """Test RecordUtil.validate method."""

    samples = [
        StubDataclassOptionalFields(id="abc7"),
        StubDataclassRecord(id="abc1"),
        StubDataclassNestedFields(id="abc2"),
        StubDataclassComposite(),
        StubDataclassDerivedRecord(id="abc3"),
        StubDataclassDerivedFromDerivedRecord(id="abc4"),
        StubDataclassOtherDerivedRecord(id="abc5"),
        StubDataclassListFields(id="abc6"),
        StubDataclassOptionalFields(id="abc7"),
        StubDataclassDictFields(id="abc8"),
        StubDataclassDictListFields(id="abc9"),
        StubDataclassListDictFields(id="abc10"),
        StubDataclassPrimitiveFields(key_str_field="abc11"),
        StubDataclassSingleton(),
    ]

    for sample in samples:
        RecordUtil.validate(sample)


if __name__ == "__main__":
    pytest.main([__file__])
