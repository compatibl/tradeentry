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
from typing import List


class FloatListUtil:
    """
    This class provides helper methods for float lists.
    """

    @classmethod
    def is_strictly_ascending(cls, values: List[float]) -> bool:
        """
        Returns true if the list is sorted in ascending order up to float
        tolerance with equal values not permitted.
        """
        tolerance: float = FloatUtil.tolerance
        arr: np.ndarray = np.array(values)
        result = np.all(arr[:-1] < arr[1:] - tolerance)
        return result

    @classmethod
    def is_equal_or_ascending(cls, values: List[float]) -> bool:
        """
        Returns true if the list is sorted in ascending order up to float
        tolerance with equal values permitted.
        """
        tolerance: float = FloatUtil.tolerance
        arr: np.ndarray = np.array(values)
        result = np.all(arr[:-1] < arr[1:] + tolerance)
        return result

    @classmethod
    def is_strictly_descending(cls, values: List[float]) -> bool:
        """
        Returns true if the list is sorted in descending order up to float
        tolerance with equal values not permitted.
        """
        tolerance: float = FloatUtil.tolerance
        arr: np.ndarray = np.array(values)
        result = np.all(arr[:-1] > arr[1:] + tolerance)
        return result

    @classmethod
    def is_equal_or_descending(cls, values: List[float]) -> bool:
        """
        Returns true if the list is sorted in descending order up to float
        tolerance with equal values permitted.
        """
        tolerance: float = FloatUtil.tolerance
        arr: np.ndarray = np.array(values)
        result = np.all(arr[:-1] > arr[1:] - tolerance)
        return result
