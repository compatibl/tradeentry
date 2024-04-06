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

from typing import List
from typing import Optional
from urllib.parse import unquote


class DatasetUtil:
    """
    Dataset class is used for validation and transformation of delimited dataset.

    By convention, dataset does not have leading or trailing path
    separator. Root dataset is represented by an empty string.

    Examples:

    * '' - root dataset has no parents
    * 'A' - single-token dataset for which parent is root dataset
    * 'A\\B' - two-token dataset for which parent is dataset A
    """

    __separator = '\\'
    __two_separators = '\\\\'

    @staticmethod
    def root() -> Optional[str]:
        """Root dataset is represented as empty string."""
        return None

    @staticmethod
    def separator() -> str:
        """Dataset separator is backslash."""
        return DatasetUtil.__separator

    @staticmethod
    def to_tokens(dataset: Optional[str]) -> List[str]:
        """
        Split delimited dataset into tokens, excluding root.
        For root dataset, this method returns an empty list.
        """
        if dataset is None or dataset == '':
            # Root dataset has no tokens
            result = []
        else:
            # If not root, split into tokens
            dataset = DatasetUtil.normalize(dataset)
            result = dataset.split(DatasetUtil.separator())

            # Validate each token
            [DatasetUtil.validate_token(token) for token in result]
        return result

    @staticmethod
    def to_lookup_list(dataset: Optional[str]) -> List[str]:
        """
        Return dataset lookup list in which the first element
        dataset value itself, followed by its parents and
        ending with root (empty) dataset.

        For root dataset, this method returns a list where
        the only element is the empty string.
        """

        # Create result which will be reversed at the end, and add root dataset
        result = [DatasetUtil.root()]

        # Return if argument is empty
        if dataset is None or dataset == '':
            return result

        # Split into tokens
        dataset_tokens = DatasetUtil.to_tokens(dataset)

        # Add incremental lookup paths each consisting of one more token than the previous one
        lookup_path = None
        result = [None]
        for token in dataset_tokens:
            if token is None or token == '':
                raise RuntimeError(f"Dataset {dataset} has empty tokens.")
            if lookup_path is None:
                lookup_path = token
            else:
                lookup_path = f"{lookup_path}{DatasetUtil.separator()}{token}"
            result.append(lookup_path)

        # Reverse to return the list ordered from child
        # to parent, beginning with argument and ending with
        # root dataset
        return list(reversed(result))

    @staticmethod
    def combine(*dataset_paths: Optional[str]) -> Optional[str]:
        """
        Combine one or more datasets paths with validation, where each path may contain more than one token.
        Empty paths are ignored.
        """
        normalized_paths = [DatasetUtil.normalize(p) for p in dataset_paths if (p is not None and p != '')]
        if len(normalized_paths) > 0:
            return DatasetUtil.__separator.join(normalized_paths)
        else:
            return None

    @staticmethod
    def normalize(dataset_path: Optional[str]) -> Optional[str]:
        """
        Error if dataset string has invalid format.

        By convention, dataset does not have leading or trailing path
        separator. Root dataset is represented by an empty string.

        Examples:

        * None - root dataset has no parents
        * 'A' - single-token dataset for which parent is root dataset
        * 'A\\B' - two-token dataset for which parent is dataset A
        """
        if dataset_path is None or dataset_path == '':
            # The value of None is valid, return without raising exception
            return None

        # Convert URL quoted unicode characters
        dataset_path = unquote(dataset_path)

        if dataset_path.startswith(DatasetUtil.__separator):
            raise Exception(f'Dataset `{dataset_path}` must not start with a backslash separator.')
        if dataset_path.endswith(DatasetUtil.__separator):
            raise Exception(f'Dataset `{dataset_path}` must not end with a backslash separator.')
        if DatasetUtil.__two_separators in dataset_path:
            raise Exception(f'Dataset `{dataset_path}` contains two backslash separators in a row.')
        if dataset_path.startswith(' '):
            raise Exception(f'Dataset `{dataset_path}` has a leading space.')
        if dataset_path.endswith(' '):
            raise Exception(f'Dataset `{dataset_path}` has a trailing space.')

        return dataset_path

    @staticmethod
    def validate_token(dataset_token: Optional[str]) -> None:
        """Validate a single dataset token."""

        if dataset_token.startswith(' '):
            raise Exception(f'Dataset token `{dataset_token}` has a leading space.')
        if dataset_token.endswith(' '):
            raise Exception(f'Dataset token `{dataset_token}` has a trailing space.')
