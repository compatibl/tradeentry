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
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.testing.regression_guard import RegressionGuard
from cl.tradeentry.entries.rates.swaps.float_swap_leg_entry import FloatSwapLegEntry


def test_float_leg_swap_entry():
    with TestingContext():
        guard = RegressionGuard()

        float_swap_leg_entry = FloatSwapLegEntry(
            description="Effective date - 10 November 2009, Tenor - 12 months, Client pays 3M Term SOFR + 70bps act/360, quarterly"
        )
        float_swap_leg_entry.run_generate()
        guard.write(str(float_swap_leg_entry))

        RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
