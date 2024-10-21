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
from cl.runtime import RecordMixin
from cl.runtime.db.protocols import TKey
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.runtime import StubDataclassRecord


class _Base(RecordMixin[StubDataclassRecord]):
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
    _Base().init_all()
    guard.write("Testing _Derived:")
    _Derived().init_all()
    guard.write("Testing _DerivedFromDerivedWithInit:")
    _DerivedFromDerivedWithInit().init_all()
    guard.write("Testing _DerivedFromDerivedWithoutInit:")
    _DerivedFromDerivedWithoutInit().init_all()
    RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
