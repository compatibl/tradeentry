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

import numpy as np

from cl.runtime.primitive.float_util import FloatUtil


class StubFloatArray:
    """Create mock samples of FloatArray."""

    @staticmethod
    def create_strictly_ascending() -> np.ndarray:
        """Create list that is sorted in ascending order with or without tolerance, and has no repeated values."""
        return np.array([1.0, 2.0, 3.0])

    @staticmethod
    def create_equal_or_ascending() -> np.ndarray:
        """Create list that is sorted in ascending order with or without tolerance, and has repeated values."""
        return np.array([1.0, 2.0, 2.0, 3.0])

    @staticmethod
    def create_equal_or_ascending_with_tolerance() -> np.ndarray:
        """
        Create list that is sorted in ascending order with tolerance,
        but unsorted without tolerance, and has repeated values.
        """
        tolerance = FloatUtil.tolerance
        return np.array([1.0, 2.0 + 0.1 * tolerance, 2.0, 2.0, 2.0 - 0.1 * tolerance, 3.0])

    @staticmethod
    def create_strictly_descending() -> np.ndarray:
        """Create list that is sorted in descending order with or without tolerance, and has no repeated values."""
        return np.array([3.0, 2.0, 1.0])

    @staticmethod
    def create_equal_or_descending() -> np.ndarray:
        """Create list that is sorted in descending order with or without tolerance, and has repeated values."""
        return np.array([3.0, 2.0, 2.0, 1.0])

    @staticmethod
    def create_equal_or_descending_with_tolerance() -> np.ndarray:
        """
        Create list that is sorted in descending order with tolerance,
        but unsorted without tolerance, and has repeated values.
        """
        tolerance = FloatUtil.tolerance
        return np.array([3.0, 2.0 - 0.1 * tolerance, 2.0, 2.0, 2.0 + 0.1 * tolerance, 1.0])
