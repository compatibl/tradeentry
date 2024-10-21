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
from cl.runtime.plots.group_bar_plot import GroupBarPlot
from cl.runtime.testing.regression_guard import RegressionGuard
from stubs.cl.convince.experiments.stub_llms import get_stub_full_llms


def _test_extraction() -> None:
    # Create Llm objects for test
    stub_full_llms = get_stub_full_llms()

    trial_count = 1
    plot_bar_labels = []
    plot_group_labels = []
    plot_values = []
    for llm in stub_full_llms:
        success_count = 0
        label = "Label"
        for trial_id in range(trial_count):
            raise NotImplementedError()
        success_fraction = min(max(round(success_count / trial_count * 100, 2), 0), 100)

        plot_bar_labels.append(llm.llm_id)
        plot_group_labels.append(label)
        plot_values.append(success_fraction)

    plot = GroupBarPlot(
        plot_id="Accuracy",
        bar_labels=plot_bar_labels,
        group_labels=plot_group_labels,
        values=plot_values,
        value_ticks=list(range(0, 101, 10)),
    )
    plot.save_png()
    RegressionGuard.verify_all()


@pytest.mark.skip("Refactoring.")
def test_end_to_end():
    with TestingContext():
        _test_extraction()


if __name__ == "__main__":
    pytest.main([__file__])
