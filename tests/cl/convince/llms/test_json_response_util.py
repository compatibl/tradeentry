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


import json
from cl.convince.llms.json_response_util import JsonResponseUtil


def test_fix_json_format():
    """Test JsonResponseUtil.fix_json_format."""

    llm_response = """{"key": 'value'}"""
    try:
        llm_response_fixed: str = JsonResponseUtil.fix_json_format(llm_response)
        llm_response_fixed = JsonResponseUtil.try_to_load_json_string(llm_response_fixed)
        llm_response_dict = json.loads(llm_response_fixed)
        print(llm_response_dict)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
