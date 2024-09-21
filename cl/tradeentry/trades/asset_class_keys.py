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

from cl.tradeentry.trades.asset_class_key import AssetClassKey


class AssetClassKeys:
    """Standard asset class keys."""

    rates: AssetClassKey = AssetClassKey(asset_class_id="Rates")
    """Interest rates asset class."""

    fx: AssetClassKey = AssetClassKey(asset_class_id="FX")
    """FX asset class."""

    equity: AssetClassKey = AssetClassKey(asset_class_id="Equity")
    """Equity asset class."""

    commodity: AssetClassKey = AssetClassKey(asset_class_id="Commodity")
    """Commodity asset class."""

    credit: AssetClassKey = AssetClassKey(asset_class_id="Credit")
    """Credit asset class."""



