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

import datetime as dt
from dataclasses import dataclass
from cl.runtime.records.dataclasses_extensions import missing
from cl.tradeentry.trades.pay_receive_enum import PayReceiveEnum
from cl.tradeentry.trades.rates.rates_leg import RatesSwapLeg


@dataclass(slots=True, kw_only=True)
class SwapLeg(RatesSwapLeg):
    """Swap leg."""

    pay_receive: PayReceiveEnum = missing()
    """String representation of the Buy or Sell flag in the format specified by the user."""

    effective_date: dt.date = missing()
    """Effective date."""

    maturity_date: dt.date = missing()
    """Maturity date."""

    payment_frequency: str = missing()
    """Payment frequency."""
