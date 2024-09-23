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
from cl.convince.llms.claude.claude_llm import ClaudeLlm
from cl.convince.llms.llama.fireworks.fireworks_llama_llm import FireworksLlamaLlm
from cl.convince.llms.gemini.gemini_llm import GeminiLlm
from cl.convince.llms.gpt.gpt_llm import GptLlm
from cl.runtime.regression.regression_guard import RegressionGuard
from utils.tag_utils import tag_text_with_numbers
from stubs.cl.tradeentry.experiments.stub_trade_entries import stub_basis_swap_entry, stub_floored_swap_entry, stub_amortizing_swap_entry

llms = [
    ClaudeLlm(llm_id="claude-3-haiku-20240307"),
    FireworksLlamaLlm(llm_id="llama-v3-70b-instruct"),
    GeminiLlm(llm_id="gemini-1.5-flash"),
    GptLlm(llm_id="gpt-4o-mini"),
]

PROMPT_TEMPLATE = """You will be given the input below in the form of a term sheet describing
some financial instrument.
Return only JSON with these keys (omit those keys that do not apply):
* InstrumentType - enum with values: AcceleratedReturnEquityLinkedNote, AutocallableEquityLinkedNote, AutocallableEquityLinkedRangeAccrualNote, AutocallableFixedRateNote, CallableEquityLinkedNote, CallableFixedForFloatingSwap, CallableFixedRateNote, CallableFloatingSpreadNote, KnockOutCommodityLinkedNote, KnockOutEquityLinkedNote, NonCallableCommodityLinkedNote, NonCallableCurrencyLinkedNote, NonCallableEquityLinkedNote, NonCallableFixedForFloatingSwap, NonCallableFixedToFloatingNote, NonCallableFloatingSpreadNote, NonCallableInflationLinkedNote.
If the Participation rate is larger than 100% select AcceleratedReturnEquityLinkedNote.

If the word "knock-out" is not used in the termsheet, do not use "KnockOutCommodityLinkedNote" nor "KnockOutEquityLinkedNote".
If the words "knock-out" and "commodity" are used in the termsheet, do use "KnockOutCommodityLinkedNote".


If the instrument can be automatically called, use one of these three instrument types:
- if the term sheet specifies an Annual Coupon Rate, then use "AutocallableFixedRateNote"
- if the term sheet contains the word "accrue" or "accrual", use "AutocallableEquityLinkedRangeAccrualNote"
- for other autocallable term sheets, use "AutocallableEquityLinkedNote".

If the term sheet does not contain the word "callable" the instrument type should not be any of the following: CallableEquityLinkedNote, CallableFixedForFloatingSwap, CallableFixedRateNote, CallableFloatingSpreadNote.

* EffectiveDate - settlement date, first calculation period start date or the first initial value determination date in yyyy-mm-dd format
* MaturityDate - last calculation period end date or last maturity determination date in yyyy-mm-dd format
* PayOrReceiveFixed - enum with values PayFixed, ReceiveFixed for a fixed for floating interest rate instrument, depending on Party A; 

* FixedRatePercent - number in percent for the fixed rate (use for the fixed leg or the entire note)
* Underlying - identifier of the underlying, or the first underlying in case there are multiple, as data vendor symbol, or if symbol is not specified then text exactly as written (applies to the floating leg or the entire note)
* Underlying2 - identifier of the second underlying in case there are multiple as data vendor symbol, or if symbol is not specified then text exactly as written (applies to the floating leg or the entire note)
* FloatingSpreadBp - number in basis points (convert from percent if necessary) for the spread over the floating index (use for the fixed leg or the entire note)
* FloatingRateMultiplier - multiplier of the floating rate used in the calculation of interest
* FloatingRateCapPct - number in percent for the floating rate cap
* FloatingRateFloorPct - number in percent for the floating rate floor
* PaymentFrequency - payment frequency for notes and instruments that have only one leg (do not specify when more than one leg is present), enum with values Annual, Semiannual, Quarterly, Monthly
* FixedLegPaymentFrequency - frequency of the fixed leg (specify only when more than one leg is present), enum with values Annual, Semiannual, Quarterly, Monthly
* FloatingLegPaymentFrequency - frequency of the floating leg  (specify only when more than one leg is present), enum with values Annual, Semiannual, Quarterly, Monthly
* Notional - number for the notional or for the principal amount per unit multiplied by the number of units for instruments with one leg (do not specify when more than one leg is present)
* FixedLegNotional - number for the notional or principal amount of the fixed leg (specify only when more than one leg is present)
* FloatingLegNotional - number for the notional or principal amount of the fixed leg (specify only when more than one leg is present)
* Currency - currency of payments in ISO-4217 format for notes and instruments with one leg (do not specify when more than one leg is present)
* FixedLegCurrency - currency of payments in ISO-4217 format of the fixed leg (specify only when more than one leg is present)
* FloatingLegCurrency - currency of payments in ISO-4217 format of the floating leg (specify only when more than one leg is present)
* ResetType - floating rate reset relative to calculation period, enum with values Upfront, InArrears
* ExerciseFrequency - exercise frequency of an embedded option, enum with values Annual, Semiannual, Quarterly, Monthly, or Daily. Daily refers to every business day.
* ParticipationRatePct - participation rate, upside leverage factor or similar parameter in percent
* CappedValueOfUnderlying - capped value of the underlying
* CappedReturnPct - capped return of the underlying in percent
* BufferAmountPct - number in percent
* TriggerLevel - price of the underlying at which knockout, knockin, or autocall occurs
* TriggerLevelPct - level of underlying at which knockout, knockin, or autocall occurs expressed as percentage of its initial value
* PrincipalProtected - enum with values Yes and No
* InitialPrice - initial price of the underlying
* RateUponTriggerPct - rate of return paid by the note in case of knockout
* CpiLagMonths - lag of the CPI index observation relative to period start or end date (use for inflation-linked instruments only)
* WorstOf - indicates the instrument is linked to the worst performance of several assets, enum with values Yes and No; if Least Performing Underlying is mentioned set to Yes.
* CUSIP - a string that uniquely identifies the instrument, in US and Canada (omit it if does not apply).

Term sheet: ```{input}```
"""


def _test_hackathon_baseline(trade_description: str):
    prompt = PROMPT_TEMPLATE.format(input=trade_description)

    with TestingContext():
        run_count = 1
        for llm in llms:
            for _ in range(run_count):
                result = llm.completion(prompt)
                guard = RegressionGuard(channel=llm.llm_id)
                guard.write(result)
        RegressionGuard.verify_all()


def test_basis_swap():
    _test_hackathon_baseline(stub_basis_swap_entry)


def test_floored_swap():
    _test_hackathon_baseline(stub_floored_swap_entry)


def test_notional_schedule_swap():
    _test_hackathon_baseline(stub_amortizing_swap_entry)


if __name__ == "__main__":
    pytest.main([__file__])
