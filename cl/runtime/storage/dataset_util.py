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

from cl.runtime.storage.data_source_types import TDataset
from cl.runtime.storage.data_source_types import TPrimitive
from typing import List
from typing import Optional
from urllib.parse import unquote


class DatasetUtil:
    """
    Utility class for dataset validation and transformation.

    Dataset can be a list of levels, a backslash-delimited string starting from backslash, or None.
    """

    _sep = "\\"
    _two_sep = "\\\\"

    @staticmethod
    def to_str(dataset: TDataset) -> str:
        """Convert the dataset from any input format to delimited string and perform validation."""

        if dataset is None:
            return DatasetUtil._sep  # Separator only if input is None or an empty string
        elif dataset == DatasetUtil._sep:
            return dataset  # Return argument if it is equal to separator
        elif isinstance(dataset, str):
            # Normalize if string
            result = DatasetUtil._normalize_str(dataset)
            return result

        elif isinstance(dataset, list):
            # Serialize and normalize levels if list
            dataset = [DatasetUtil._normalize_level(x, dataset) for x in dataset]

            # Concatenate and return
            dataset_str = DatasetUtil._sep + DatasetUtil._sep.join(dataset)
            return dataset_str

        else:
            raise RuntimeError(f"Dataset {dataset} is not a delimited string, list of levels, or None.")

    @staticmethod
    def to_levels(dataset: TDataset) -> List[str]:
        """Convert the dataset from any input format to a list of levels and perform validation."""

        if dataset is None or dataset == DatasetUtil._sep:
            return []  # Root dataset has no levels

        elif isinstance(dataset, str):
            # Convert URL quoted unicode characters
            dataset = unquote(dataset)

            # Split and remove thr first level after checking it is empty
            dataset = dataset.split(DatasetUtil._sep)
            if len(dataset) < 2 or dataset[0] != "":
                raise RuntimeError(f"Dataset {dataset} does not start from the separator {DatasetUtil._sep}.")
            dataset = dataset[1:]

        if isinstance(dataset, list):
            # Validate all levels
            [DatasetUtil._normalize_level(level) for level in dataset]
        else:
            raise RuntimeError(f"Dataset {dataset} is not a delimited string, list of levels, or None.")

        return dataset

    @staticmethod
    def to_lookup_list(dataset: TDataset) -> List[str]:
        """
        Convert the dataset in any format to a list of datasets in string format.
        Each element of the returned list represents one step in a hierarchical lookup
        starting from the argument dataset and ending with the root dataset.
        """

        # Convert to levels
        levels = DatasetUtil.to_levels(dataset)

        # Each element of this list has one less level, starting from the original list and ending with empty list
        list_of_lists = [levels[: len(levels) - i] for i in range(len(levels) + 1)]

        # Convert each list element to string format
        result = [DatasetUtil.to_str(dataset) for dataset in list_of_lists]
        return result

    @staticmethod
    def combine(*datasets: TDataset) -> TDataset | None:
        """
        Combine one or more datasets paths with validation, where each path may contain more than one level.
        Returns dataset as a list of levels.
        """

        if len(datasets) == 0:
            raise RuntimeError("No arguments were passed to DatasetUtil.combine method.")

        # Validate and convert to
        datasets = [DatasetUtil.to_levels(p) for p in datasets]

        # Merge lists, no further validation is required
        result = [level for dataset in datasets for level in dataset]
        return result

    @staticmethod
    def _normalize_str(dataset: str) -> str:
        """
        Normalize a dataset provided in string format by converting URL quoted unicode characters.
        Validates that the dataset consists of backslash delimited levels with leading backslash.
        """

        if not isinstance(dataset, str):
            raise RuntimeError(f"Method DatasetUtil.normalize(str) is applied to non-string dataset {dataset}.")

        # Convert URL quoted unicode characters
        dataset = unquote(dataset)

        if not dataset.startswith(DatasetUtil._sep):
            raise Exception(f"Dataset `{dataset}` does not start with a backslash separator.")
        if dataset.endswith(DatasetUtil._sep):
            raise Exception(f"Dataset `{dataset}` must not end with a backslash separator.")
        if DatasetUtil._two_sep in dataset:
            raise Exception(f"Dataset `{dataset}` contains two backslash separators in a row.")
        if dataset.startswith(" "):
            raise Exception(f"Dataset `{dataset}` has a leading space.")
        if dataset.endswith(" "):
            raise Exception(f"Dataset `{dataset}` has a trailing space.")

        return dataset

    @staticmethod
    def _normalize_level(level: TPrimitive, dataset: TDataset = None) -> str:
        """
        Serialize or convert URL quoted unicode characters and validate a single dataset level.
        Takes complete dataset as an optional argument to use in error reporting only.
        """

        # Validate
        if level is None:
            in_dataset = DatasetUtil._in_dataset_msg(dataset)
            raise Exception(f"A dataset level{in_dataset}is None.")

        elif isinstance(level, str):
            # Convert URL quoted unicode characters
            level = unquote(level)

            # Validate string level format
            if level == "":
                in_dataset = DatasetUtil._in_dataset_msg(dataset)
                raise Exception(f"A dataset level{in_dataset}is an empty string.")
            if DatasetUtil._sep in level:
                in_dataset = DatasetUtil._in_dataset_msg(dataset)
                raise Exception(f"Dataset level '{level}'{in_dataset}contains backslash separator.")
            if level.startswith(" "):
                in_dataset = DatasetUtil._in_dataset_msg(dataset)
                raise Exception(f"Dataset level '{level}'{in_dataset}has a leading space.")
            if level.endswith(" "):
                in_dataset = DatasetUtil._in_dataset_msg(dataset)
                raise Exception(f"Dataset level '{level}'{in_dataset}has a trailing space.")

            return level

        elif isinstance(level, int):
            # TODO: Support the remaining primitive types and provide serialization
            level = str(level)
            return level

        else:
            in_dataset = DatasetUtil._in_dataset_msg(dataset)
            raise Exception(f"A dataset level '{str(level)}'{in_dataset}is not one of the permitted primitive types.")

    @staticmethod
    def _in_dataset_msg(dataset: TDataset) -> str:
        """Form part of an error message containing full dataset."""

        # Convert whole_dataset to an error message segment
        if dataset is None or dataset == "":
            # Single space if dataset is None or empty
            return " "
        elif is_list := isinstance(dataset, list) or isinstance(dataset, str):
            if is_list:
                # Concatenate *without validation* if dataset is provided in list format
                dataset = [str(x) for x in dataset]
                dataset = DatasetUtil._sep + DatasetUtil._sep.join(dataset)

            # Convert URL quoted unicode characters and return
            dataset = unquote(dataset)
            return f" in '{dataset}' "
        else:
            raise RuntimeError(f"Dataset {dataset} is not a delimited string, list of levels, or None.")
