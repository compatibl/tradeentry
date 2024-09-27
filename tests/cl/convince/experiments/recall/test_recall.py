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
import datetime as dt
from random import Random
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.convince.experiments.stub_llms import get_stub_mini_llms


def _test_recall(text: str):
    """Test the specified recall string."""

    with TestingContext():

        prompt = (
            f"Reply with the following text changing nothing in it at all. "
            f"I will check that the text matches exactly. This is a test. Text: {text}"
        )
        run_count = 1

        stub_mini_llms = get_stub_mini_llms()
        for llm in stub_mini_llms:
            guard = RegressionGuard(channel=llm.llm_id)
            for _ in range(run_count):

                result = llm.completion(prompt)
                guard.write(result)

        guard.verify_all()


def test_well_known_phrase():
    """Test a well-known recall string."""
    _test_recall("A quick brown fox jumps over the lazy dog")


def test_modified_well_known_phrase():
    """Test the specified recall string."""
    _test_recall("A quick brown fox jumps over a lazy dog")


def test_date_list():
    """Test random dates."""
    origin_date = dt.date(2003, 4, 21)
    date_count = 10
    max_offset = 10_000

    # Create a random generator with seed
    randgen = Random(0)

    offsets = [randgen.randint(0, max_offset) for _ in range(date_count)]
    date_list = [origin_date + dt.timedelta(days=offset) for offset in offsets]
    date_list_str = ",".join(DateUtil.to_str(date) for date in date_list)
    _test_recall(date_list_str)


if __name__ == "__main__":
    pytest.main([__file__])
