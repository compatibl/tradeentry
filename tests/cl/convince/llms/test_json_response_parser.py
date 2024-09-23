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


import orjson as json
import regex as re


def sanitize_unescaped_quotes_and_load_json_str(s: str, strict: bool = False) -> str:
    js_str = s
    max_replaces = s.count('"')

    if not max_replaces:
        json.loads(js_str)
        return js_str

    prev_pos = -1
    curr_pos = 0

    while curr_pos > prev_pos and max_replaces > 0:
        max_replaces -= 1
        # after while check, move marker before we overwrite it
        prev_pos = curr_pos
        try:
            json.loads(js_str)
            return js_str
        except json.JSONDecodeError as err:
            curr_pos = err.pos
            if curr_pos <= prev_pos:
                break

            # find the previous " before e.pos
            prev_quote_index = js_str.rfind('"', 0, curr_pos)
            if prev_quote_index > 1 and js_str[prev_quote_index - 1] == "\\":
                # if the previous " is escaped, ignore it
                prev_pos = curr_pos
                continue

            # escape it to \"
            js_str = js_str[:prev_quote_index] + "\\" + js_str[prev_quote_index:]
    if strict:
        raise ValueError("Unable to sanitize unescaped quotes in the provided string to a valid JSON!")
    return "{}"


def extract_json_content(json_string: str) -> str:
    """Remove all symbols up to the first `{` and all symbols after the last `}` from a JSON string."""

    # Find the first and last occurrences of `{` and `}`
    first_curly_bracket = json_string.find("{")
    last_curly_bracket = json_string.rfind("}")

    # Ensure that both curly brackets were found
    if first_curly_bracket != -1 and last_curly_bracket != -1:
        first_square_bracket = json_string.find("[", 0, first_curly_bracket)
        last_square_bracket = json_string.rfind("]", last_curly_bracket, len(json_string))

        if first_square_bracket != -1 and last_square_bracket != -1:
            # Extract the substring between the square brackets, it is an array
            return json_string[first_square_bracket : last_square_bracket + 1]
        elif first_square_bracket == -1 and last_square_bracket == -1:
            # Extract the substring between the curly brackets, it is an object
            return json_string[first_curly_bracket : last_curly_bracket + 1]

    # Return original string in case one or both opened and closed curly brackets were not found
    return json_string


def fix_json_format(json_string: str) -> str:
    """Fix JSON quotes and values."""

    # Remove all the symbols before the first opened bracket and after the last closed,
    # in particular, '''json<actual_json>''' wrap.
    fixed_json_string = extract_json_content(json_string)

    temp_str = "__TEMP__"

    # Fix apostrophes and single quotes
    # This regex patterns uses positive lookbehind to ensure that the apostrophe is preceded by a word character
    # and positive lookahead to ensure it's followed by a word character.
    # This way, it will match only the apostrophes used as contractions or possessive form.
    #
    # sample_string = 'He's going to the doctor\'s office on his brothers' motorcycle.'
    # fixed_string  = 'He{temp_str}s going to the doctor{temp_str}s office on his brothers{temp_str} motorcycle.'
    fixed_json_string = re.sub(r"(?<=\w)'(?=\w)", temp_str, fixed_json_string)  # It's
    fixed_json_string = re.sub(r"(?<=\w)\\'(?=\w)", temp_str, fixed_json_string)  # It\'s
    fixed_json_string = re.sub(r"(?<=s)'(?=\s)", temp_str, fixed_json_string)  # Its'_  (_ is space)
    fixed_json_string = re.sub(r"(?<=s)\\'(?=\s)", temp_str, fixed_json_string)  # Its\'_  (_ is space)

    # Replace all remaining single quotes with double quotes
    fixed_json_string = fixed_json_string.replace("'", '"')

    # Replace {temp_str} back to single quotes
    fixed_json_string = fixed_json_string.replace(temp_str, "'")

    # Fix boolean and None values
    fixed_json_string = fixed_json_string.replace("True", "true")
    fixed_json_string = fixed_json_string.replace("False", "false")
    fixed_json_string = fixed_json_string.replace('"None"', "None")
    # Use the following regex to replace None with "None".
    # `fixed_json_string.replace('"None"', 'None')` won't work,
    # because LLM output value may contain something like: "None of the above"
    fixed_json_string = re.sub(r'(?<="[^"]+":\s*)None', '"None"', fixed_json_string)

    # Fix trailing comma before closing brace
    fixed_json_string = re.sub(r",\s*\}", " }", fixed_json_string)

    # Fix unnecessary escaped underscores
    fixed_json_string = fixed_json_string.replace("\\_", "_")

    fixed_json_string = fixed_json_string.replace("\\n", "\n")

    fixed_json_string = fixed_json_string.replace('\\"', "'")

    return fixed_json_string


def _try_to_load_json_string(json_string: str) -> str:
    """Try to load the provided json string. In case of success, return str, otherwise raise JSONDecodeError."""
    try:
        # try to load the provided json string firstly
        json.loads(json_string)
        return json_string
    except json.JSONDecodeError:
        # in case of exception, try to sanitize quotes and load it once again
        try:
            sanitized_string = sanitize_unescaped_quotes_and_load_json_str(json_string, strict=True)
            json.loads(sanitized_string)
            return sanitized_string
        except ValueError:
            # Llm might not fully understand an exception message
            # that is raised in sanitize_unescaped_quotes_and_load_json_str function
            # so, we pass this exception and relay on the original one re-raising it
            pass
        raise


def test_fix_llm_response():
    llm_response = """{"key": 'value'}"""
    try:
        llm_response_fixed: str = fix_json_format(llm_response)
        llm_response_fixed = _try_to_load_json_string(llm_response_fixed)
        llm_response_dict = json.loads(llm_response_fixed)
        print(llm_response_dict)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
