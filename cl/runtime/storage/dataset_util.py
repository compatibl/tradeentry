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
from cl.runtime.primitive.date_util import DateUtil
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.storage.data_source_types import TPrimitive
from typing import List, Iterable
from urllib.parse import unquote


class DatasetUtil:
    """
    Utility class for dataset validation and transformation.

    Dataset can be a list of levels, a backslash-delimited string starting from backslash, or None.
    """

    _sep = "\\"
    _two_sep = "\\\\"

    @classmethod
    def to_levels(cls, dataset: str) -> List[str]:
        """Convert the dataset from any input format to a list of levels and perform validation."""

        if dataset is None or dataset == DatasetUtil._sep:
            return []  # Root dataset has no levels

        elif isinstance(dataset, str):
            # Convert URL quoted unicode characters
            dataset = unquote(dataset)

            # Remove leading separator if present
            if dataset.startswith(cls._sep):
                dataset = dataset.removeprefix(cls._sep)

            # Split into levels according to the separator
            dataset = dataset.split(DatasetUtil._sep)

        if hasattr(dataset, "__iter__"):
            # Validate all levels
            [DatasetUtil._normalize_level(level) for level in dataset]
        else:
            raise RuntimeError(f"Dataset {dataset} is not a delimited string, iterable of strings, or None.")

        return dataset

    @classmethod
    def to_lookup_list(cls, dataset: str) -> List[str]:
        """
        Convert the dataset in any format to a list of datasets in string format.
        Each element of the returned list represents one step in a hierarchical lookup
        starting from the argument dataset and ending with the root dataset.
        """

        # Convert to levels
        levels = DatasetUtil.to_levels(dataset)

        # Each element of this list has one less level, starting from the original list and ending with empty list
        list_of_partial_lists = [levels[: len(levels) - i] for i in range(len(levels) + 1)]

        # Convert each list element to string format
        result = [DatasetUtil.combine(*partial_list) for partial_list in list_of_partial_lists]
        return result

    @classmethod
    def combine(cls, *datasets: TPrimitive | Iterable[TPrimitive] | None) -> str:
        """
        Combine one or more datasets with validation, where each argument may contain more than one level.

        Notes:
            - The arguments may optionally begin from dataset separator (backslash)
            - Arguments that are None are disregarded
        """

        # Return root dataset if no parameters are passed
        if len(datasets) == 0:
            return cls._sep

        # Convert non-empty tokens to levels with validation
        arg_levels = [DatasetUtil.to_levels(p) for p in datasets if p is not None]

        # Merge lists
        all_levels = [level for dataset in arg_levels if dataset is not None for level in dataset if level is not None]

        # Convert to string
        result = DatasetUtil._sep + DatasetUtil._sep.join(all_levels)
        return result

    @classmethod
    def _normalize_str(cls, dataset: str) -> str:
        """
        Normalize a dataset provided in string format by converting URL quoted unicode characters.
        Validates that the dataset consists of backslash delimited levels with leading backslash.
        """

        if not isinstance(dataset, str):
            raise RuntimeError(f"Method DatasetUtil.normalize(str) is applied to non-string dataset {dataset}.")

        # Convert URL quoted unicode characters
        dataset = unquote(dataset)

        if not dataset.startswith(DatasetUtil._sep):
            raise Exception(f"Dataset '{dataset}' does not start with a backslash separator.")
        if dataset.endswith(DatasetUtil._sep):
            raise Exception(f"Dataset '{dataset}' must not end with a backslash separator.")
        if DatasetUtil._two_sep in dataset:
            raise Exception(f"Dataset '{dataset}' contains two backslash separators in a row.")
        if dataset.startswith(" "):
            raise Exception(f"Dataset '{dataset}' has a leading space.")
        if dataset.endswith(" "):
            raise Exception(f"Dataset '{dataset}' has a trailing space.")

        return dataset

    @classmethod
    def _normalize_level(cls, dataset_level: TPrimitive | None) -> str:
        """Validate and convert input to a single dataset level."""

        if isinstance(dataset_level, str):
            # Convert URL quoted unicode characters
            dataset_level = unquote(dataset_level)

            # Validate string level format
            if dataset_level == "":
                raise Exception(f"A dataset level is an empty string.")
            if DatasetUtil._sep in dataset_level:
                raise Exception(f"Dataset level '{dataset_level}' includes backslash. This is not allowed "
                                f"because backslash also serves as a level separator.")
            if dataset_level.startswith(" "):
                raise Exception(f"Dataset level '{dataset_level}' has a leading space.")
            if dataset_level.endswith(" "):
                raise Exception(f"Dataset level '{dataset_level}' has a trailing space.")

            return dataset_level

        elif isinstance(dataset_level, dt.date):
            # Convert to ISO-8601 format for date (yyyy-mm-dd)
            return DateUtil.to_str(dataset_level)
        elif isinstance(dataset_level, dt.datetime):
            # Convert to ISO-8601 format for datetime (yyyy-mm-dd) with validation
            # Datetime must be rounded to milliseconds and in UTC timezone
            return DatetimeUtil.to_str(dataset_level)
        else:
            # TODO: Add other primitive types
            raise Exception(f"Dataset level '{str(dataset_level)}' has type {type(dataset_level)} which is not "
                            f"one of the permitted dataset token types or their iterable.")
