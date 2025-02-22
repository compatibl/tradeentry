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

from cl.tradeentry.trades.pay_receive_fixed_key import PayReceiveFixedKey

cls = PayReceiveFixedKey


class PayReceiveFixedKeys:
    """PayReceiveFixedKey constants."""

    PAY_FIXED: cls = cls(pay_receive_fixed_id="PayFixed")
    """We pay fixed leg coupons."""

    RECEIVE_FIXED: cls = cls(pay_receive_fixed_id="ReceiveFixed")
    """We receive fixed leg coupons."""
