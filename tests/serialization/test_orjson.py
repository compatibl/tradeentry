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
import orjson
import tests

# Tests for orjson package to ensure package upgrades to not break the code


def test_smoke():
    """Smoke test."""

    # OPT_NAIVE_UTC: Interpret datetime without tzinfo as UTC
    # OPT_UTC_Z: Append Z to datetime
    # OPT_STRICT_INTEGER: Error on integers exceeding (+/-) 2^53 - 1 = 9007199254740991 to ensure JS compatibility
    # OPT_SERIALIZE_NUMPY: Serialize numpy arrays
    options = orjson.OPT_NAIVE_UTC | orjson.OPT_UTC_Z | orjson.OPT_STRICT_INTEGER | orjson.OPT_SERIALIZE_NUMPY

    # OPT_INDENT_2: Pretty-print with indent=2
    print_options = options | orjson.OPT_INDENT_2 | orjson.OPT_APPEND_NEWLINE

    # Create test dictionary and serialize
    dict_data = tests.MockDictUtil.create()
    json_bytes = orjson.dumps(dict_data, option=options)
    deserialized_data = orjson.loads(json_bytes)
    # TODO: Implement taking into account that deserialized JSON includes some types as strings
    #   assert dict_data == deserialized_data

    # With pretty print
    pretty_print_bytes = orjson.dumps(dict_data, option=print_options)
    deserialized_pretty_print_data = orjson.loads(pretty_print_bytes)
    # TODO: Implement taking into account that deserialized JSON includes some types as strings
    #   assert dict_data == deserialized_pretty_print_data


if __name__ == '__main__':
    pytest.main([__file__])
