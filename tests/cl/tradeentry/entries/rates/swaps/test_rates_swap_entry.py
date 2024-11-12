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
from cl.tradeentry.entries.rates.swaps.rates_swap_entry import RatesSwapEntry
from cl.tradeentry.entries.rates.swaps.vanilla_swap_entry import VanillaSwapEntry
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_fixed_for_floating_swap_entry


def test_rates_swap_entry():
    """Test the leg creation process using the temporal logic of the run_generate function."""

    with TestingContext():
        guard = RegressionGuard()

        fixed_for_floating_swap_description = """Swap Details, Notional - 10,000,000,000, Bank pays - 6M USD Term SOFR, semi-annual, act/360, Bank receives - USD fixed 3.45%, semi-annual, act/360, Notional exchange -  None, Start date - 10 November 2009, Tenor - 5y"""
        rates_swap_entry = RatesSwapEntry(description=fixed_for_floating_swap_description)
        rates_swap_entry.run_generate()
        guard.write(str(rates_swap_entry))

        RegressionGuard.verify_all()


if __name__ == "__main__":
    pytest.main([__file__])
