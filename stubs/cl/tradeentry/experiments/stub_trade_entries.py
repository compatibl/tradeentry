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

stub_vanilla_swap_entry = """Sell 10y SOFR swap at 3.45%"""

stub_fixed_for_floating_swap_entry = """Swap Details:
Notional: 10,000,000,000
Bank pays: 6M USD Term SOFR, semi-annual, act/360
Bank receives: USD fixed 3.45%, semi-annual, act/360
Notional exchange: None
Start date: 10 November 2009
Tenor: 5y"""

stub_basis_swap_entry = """Floating vs Floating Swap
Start date: 10 November 2009
Tenor: 12 months
Notional: USD 10,000,000.00
Client pays 3M Term SOFR + 70bps (act/360, quarterly)
Client receives 12M Term SOFR (act/360, annual)"""

stub_floored_swap_entry = """Floored USD IRS Swap
Notional: USD 1bn
We pay: 6M USD Term SOFR (floating), semi-annual, act/360
We receive: USD fixed 3.45%, semi-annual, act/360
Notional exchange: None
Start: 10 November 2009
Tenor: 5 years
Floor: We sell a USD floor at zero (6M USD Term SOFR)"""

stub_amortizing_swap_entry = """Notional: amortizing, as per schedule below
Party A pays: 6M USD Term SOFR (floating), semi-annual, act/360
Party A receives: USD fixed 3.20%, semi-annual, act/360
Notional exchange: None
Start: 10 November 2009
Tenor: 5 years
Notional Schedule
Notional Amount Schedule	
Effective From: Notional Amount: (USD)
10-Nov-09 100,000,000.00
10-May-10 100,000,000.00
10-Nov-10 100,000,000.00
10-May-11 100,000,000.00
10-Nov-11 90,000,000.00
10-May-12 80,000,000.00
10-Nov-12 70,000,000.00
10-May-13 60,000,000.00
10-Nov-13 50,000,000.00
10-May-14 25,000,000.00"""
