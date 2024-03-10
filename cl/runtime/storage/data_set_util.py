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


class DataSetUtil:
    """
    Dataset is specified using a forward slash (/) delimited string similar to Linux directory.
    The lookup is performed in the dataset itself first, and then in each parent up to and
    including the root dataset.

    Formatting:

    - The dataset string must have a leading forward slash but not a trailing forward slash
    - Two forward slashes are not allowed
    - Trailing and leading space is not allowed for the dataset or its tokens, but space inside tokens is allowed
    - Root dataset is represented by a single forward slash

    Examples:

    - Root dataset: '/'
    - Single-level dataset for which root dataset is the parent: '/A'
    - Two-level dataset for which '/A' is the parent: '/A/B'
    """

    @staticmethod
    def root() -> str:
        """Root dataset is represented as a single slash similar to the root directory on Linux."""
        return '/'

    @staticmethod
    def to_tokens(data_set: str) -> List[str]:
        """
        Split dataset into tokens in the order specified, validating formatting of each token.
        
        Examples:
    
        - Root dataset: '/' -> []
        - Single-level dataset for which root dataset is the parent: '/A' -> ["A"]
        - Two-level dataset for which '/A' is the parent: '/A/B' -> ["A", "B"]
        """

        # Checks for the entire dataset string
        if data_set is None or data_set == "":
            raise Exception("Dataset is empty.")
        if not data_set.startswith('/'):
            raise Exception(f"Dataset {data_set} is invalid because it does not have a leading slash.")
        if not data_set == '/' and data_set.endswith('/'):
            raise Exception(f"Dataset {data_set} is invalid because it has a trailing slash.")
        if '//' in data_set:
            raise Exception(f"Dataset {data_set} is invalid because it has two slashes in a row.")

        if data_set == '/':

            # Empty list for the root dataset
            return []

        else:

            # Otherwise one element of list per level below root
            # Remove leading slash before split
            tokens = data_set[1:].split('/')

            # Check each token
            if any(token.startswith(' ') for token in tokens):
                raise Exception(f"Dataset {data_set} is invalid because one of its tokens has a leading space.")
            if any(token.endswith(' ') for token in tokens):
                raise Exception(f"Dataset {data_set} is invalid because one of its tokens has a trailing space.")

            return tokens

    @staticmethod
    def from_tokens(tokens: List[str]) -> str:
        """
        Create dataset string from tokens in the order specified, validating the formatting of each token.
        
        Examples:
    
        - Root dataset: '/' -> []
        - Single-level dataset for which root dataset is the parent: '/A' -> ["A"]
        - Two-level dataset for which '/A' is the parent: '/A/B' -> ["A", "B"]
        """

        # Check each token
        if any(token is None or token == "" for token in tokens):
            raise Exception(f"The list of dataset tokens {tokens} is invalid because it has an empty token.")
        if any('/' in token for token in tokens):
            raise Exception(f"The list of dataset tokens {tokens} is invalid because a token contains forward slash.")
        if any(token.startswith(' ') for token in tokens):
            raise Exception(f"The list of dataset tokens {tokens} is invalid a token has a leading space.")
        if any(token.endswith(' ') for token in tokens):
            raise Exception(f"The list of dataset tokens {tokens} is invalid a token has a trailing space.")

        result = '/' + '/'.join(tokens)
        return result

    @staticmethod
    def to_lookup_list(data_set: str) -> List[str]:
        """
        Return dataset lookup list in which the first element is the dataset itself,
        followed by its parents and ending with root dataset.
        """

        # Create result which will be reversed at the end, and add root dataset
        result = ['/']

        # Create dataset builder and add levels one by one
        tokens = DataSetUtil.to_tokens(data_set)
        for token in tokens:
            # TODO: Implement
            raise NotImplementedError()

        # Reverse to return the list ordered from child
        # to parent, beginning with argument and ending with
        # root dataset
        return list(reversed(result))
