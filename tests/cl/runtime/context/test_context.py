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
from cl.runtime import DataSource
from cl.runtime.context.context import Context
from stubs.cl.runtime.records.for_dataclasses.stub_dataclass_record import StubDataclassRecord


def test_smoke():
    """Smoke test."""

    # TODO: Check that calling Context.current() here raises an error if called here

    with Context() as current_context_1:

        # Check that current context is set inside 'with Context(...)' clause
        assert Context.current() is current_context_1

        # Check that creating a context object but not using it in 'with Context()'
        # clause does not change the current context
        other_context = Context()
        # Still the same current context
        assert Context.current() is current_context_1

        with Context() as current_context_2:
            # New current context
            assert Context.current() is current_context_2

        # After exiting the second 'with' clause, the previous current context is restored
        assert Context.current() is current_context_1

    # TODO: Check that calling Context.current() here raises an error if called here


if __name__ == "__main__":
    pytest.main([__file__])
