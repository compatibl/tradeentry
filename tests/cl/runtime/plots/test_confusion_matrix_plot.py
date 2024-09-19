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

from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from cl.runtime.plots.matrix_util import MatrixUtil
from cl.runtime.plots.confusion_matrix_plot import ConfusionMatrixPlot, YELLOW_TO_WHITE
from cl.runtime.testing.pytest.pytest_fixtures import local_dir_fixture


def test_absolute(local_dir_fixture):
    raw_data = pd.read_csv(Path(__file__).resolve().parent / './test_confusion_matrix_plot.csv')

    data_confusion_matrix = MatrixUtil.create_confusion_matrix(
        data=raw_data, true_column_name='True Category', predicted_column_name='Predicted'
    )
    data_confusion_matrix_percent = MatrixUtil.convert_confusion_matrix_to_percent(data=data_confusion_matrix)
    annotation_text = MatrixUtil.create_confusion_matrix_labels(data=data_confusion_matrix)

    fig = ConfusionMatrixPlot.plot_confusion_matrix(data=data_confusion_matrix_percent, annotation_text=annotation_text)
    fig.write_image("test_confusion_matrix_plot.test_absolute.png")


def test_percent(local_dir_fixture):
    raw_data = pd.read_csv(Path(__file__).resolve().parent / './test_confusion_matrix_plot.csv')

    data_confusion_matrix = MatrixUtil.create_confusion_matrix(
        data=raw_data, true_column_name='True Category', predicted_column_name='Predicted'
    )
    data_confusion_matrix_percent = MatrixUtil.convert_confusion_matrix_to_percent(data=data_confusion_matrix)
    annotation_text = MatrixUtil.create_confusion_matrix_labels(data=data_confusion_matrix, in_percent=True)

    fig = ConfusionMatrixPlot.plot_confusion_matrix(data=data_confusion_matrix_percent, annotation_text=annotation_text)
    fig.write_image("test_confusion_matrix_plot.test_percent.png")


def test_white_to_yellow(local_dir_fixture):
    raw_data = pd.read_csv(Path(__file__).resolve().parent / './test_confusion_matrix_plot.csv')

    data_confusion_matrix = MatrixUtil.create_confusion_matrix(
        data=raw_data, true_column_name='True Category', predicted_column_name='Predicted'
    )
    data_confusion_matrix_percent = MatrixUtil.convert_confusion_matrix_to_percent(data=data_confusion_matrix)
    annotation_text = MatrixUtil.create_confusion_matrix_labels(data=data_confusion_matrix, in_percent=True)

    fig = ConfusionMatrixPlot.plot_confusion_matrix(
        data=data_confusion_matrix_percent,
        annotation_text=annotation_text,
        diag_colorscale=YELLOW_TO_WHITE,
        diag_text_color_threshold=1
    )
    fig.write_image("test_confusion_matrix_plot.test_white_to_yellow.png")


def test_white_to_red(local_dir_fixture):
    raw_data = pd.read_csv(Path(__file__).resolve().parent / './test_confusion_matrix_plot.csv')

    data_confusion_matrix = MatrixUtil.create_confusion_matrix(
        data=raw_data, true_column_name='True Category', predicted_column_name='Predicted'
    )
    data_confusion_matrix_percent = MatrixUtil.convert_confusion_matrix_to_percent(data=data_confusion_matrix)
    diag_mask = np.eye(data_confusion_matrix_percent.shape[0], dtype=bool)
    data_confusion_matrix_error_percent = data_confusion_matrix_percent.copy()
    data_confusion_matrix_error_percent.values[diag_mask] = 100 - np.diag(data_confusion_matrix_percent)
    annotation_text = MatrixUtil.create_confusion_matrix_labels(data=data_confusion_matrix, in_percent=True)

    fig = ConfusionMatrixPlot.plot_matrix(
        data=data_confusion_matrix_error_percent,
        annotation_text=annotation_text
    )
    fig.write_image("test_confusion_matrix_plot.test_white_to_red.png")


if __name__ == "__main__":
    pytest.main([__file__])
