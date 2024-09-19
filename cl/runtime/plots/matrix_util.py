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

from typing import List, Optional

import pandas as pd

from sklearn.metrics import confusion_matrix


class MatrixUtil:

    @staticmethod
    def create_confusion_matrix(
            data: pd.DataFrame,
            true_column_name: str,
            predicted_column_name: str
    ) -> pd.DataFrame:
        categories = data[true_column_name].unique().tolist()
        data_confusion_matrix = confusion_matrix(
            y_true=data[true_column_name], y_pred=data[predicted_column_name], labels=categories
        )

        result = pd.DataFrame(data_confusion_matrix, index=categories, columns=categories)

        return result

    @staticmethod
    def convert_confusion_matrix_to_percent(data: pd.DataFrame) -> pd.DataFrame:
        # convert to percents row-wise
        result = data / data.values.sum(axis=1) * 100

        return result

    @staticmethod
    def create_confusion_matrix_labels(data: pd.DataFrame, in_percent: Optional[bool] = False) -> List[List[str]]:
        # str of each non-zero element of data for annotations

        if in_percent:
            data_percent = data.values / data.values.sum(axis=1) * 100
            annotation_text = [[f'{y:.2f}%' if y != 0 else '' for y in x] for x in data_percent]
        else:
            annotation_text = [[str(y) if y != 0 else '' for y in x] for x in data.values]

        return annotation_text
