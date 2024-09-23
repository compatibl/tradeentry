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

import re
from typing import Dict, List, Union


class StubTradeChecker:
    def __init__(self, input_rows: List[str]):
        self.input_rows = input_rows

    def check_row(self, _row: str, field: str) -> Dict:
        try:
            pos = int(_row[: _row.index(":")])
        except ValueError:
            return {"message": "ERROR: can't extract row number", "output_row": _row}
        try:
            true_row = self.input_rows[pos - 1]
        except IndexError:
            return {"message": "ERROR: pos is out of range, check row enumeration", "pos": pos, "row": _row}
        try:
            pos_true = int(true_row[: true_row.index(":")])
        except ValueError:
            return {"message": "The input row is not indexed, check row enumeration", "input_row": true_row}
        if pos_true != pos:
            return {
                "message": "The input and output row positions do not match, check row enumeration",
                "output_row": _row,
                "input_row": true_row,
            }

        match = re.search(f"(.*?)<{field}>(.*?)</{field}>(.*)", _row)
        if match is None:
            return {"message": "ERROR: can't find tag pair using regex.", "output_row": _row}

        target_row = "".join(match.groups())
        if true_row != target_row:
            return {
                "message": "ERROR: the rows are not the same",
                "input_row": true_row,
                "extracted_row": target_row,
                "output_row": _row,
            }

        return {}

    def field_correctness(self, fields: List[Dict], json_output: Dict, trade_desc: str) -> Dict:
        result = {}
        field_names_to_pos = {x["name"]: i for i, x in enumerate(fields)}
        trade_desc_rows = trade_desc.split("\n")

        for field in json_output:
            if field not in field_names_to_pos:
                result[field] = {
                    "error_messages": [{"message": "ERROR: There is no such field in the description."}],
                    "status": "TERRIBLE",
                }
                continue

            field_output = json_output[field]
            field_desc = fields[field_names_to_pos[field]]

            if isinstance(field_output, list):
                error_messages = []
                if field_desc["freq"] != "multiple":
                    error_messages.append({"message": "ERROR: wrong freq of answer, should be multiple"})
                for row in field_output:
                    error_message = self.check_row(row, field)
                    if error_message:
                        error_messages.append(error_message)
                result[field] = {"error_messages": error_messages, "status": "BAD" if error_messages else "OK"}
            elif isinstance(field_output, str):
                error_messages = []
                if field_desc["freq"] != "single":
                    error_messages.append({"message": "ERROR: wrong freq of answer, should be single"})
                error_message = self.check_row(field_output, field)
                if error_message:
                    error_messages.append(error_message)
                result[field] = {"error_messages": error_messages, "status": "BAD" if error_messages else "OK"}
            else:
                result[field] = {
                    "error_messages": [{"message": "ERROR: The answer is in the wrong format"}],
                    "status": "TERRIBLE",
                }

        for field in fields:
            name = field["name"]
            if name not in json_output:
                result[name] = {
                    "error_messages": [{"message": "ERROR: Missing required field", "field": name}],
                    "status": "NOT GOOD",
                }

        error_count = sum(1 for value in result.values() if value["status"] != "OK")
        result["_error_count"] = error_count

        return result


class StubFormattedStringChecker:
    def __init__(self, trade_description: str, field_description: List[Dict]):
        self.trade_description_rows = self._get_rows_from_numbered_text(trade_description)
        self.field_freq = {
            field["name"]: field["freq"]
            for field in field_description
        }

    @staticmethod
    def _extract_row_number(row: str) -> int:
        try:
            row_num = int(row[:row.index(':')])
        except:
            raise TypeError(f"Can not extract row number for row {row}")
        return row_num

    @staticmethod
    def _get_rows_from_numbered_text(text: str) -> Dict:
        rows = text.split('\n')
        answer = dict()
        for row in rows:
            row_num = StubFormattedStringChecker._extract_row_number(row)
            answer[row_num] = row
        return answer

    def check_field_piece(self, field: str, answer: Union[List, Dict]) -> Dict:
        if not answer["data"] and not answer["formatted_row"]:
            return dict()
        if not isinstance(answer["data"], str):
            return {
                "message": f"ERROR: answer data is not string type",
                "type": str(type(answer["data"])),
                "data": answer["data"]
            }
        template = '{' + field + '}'
        if template not in answer["formatted_row"]:
            return {
                "message": f"ERROR: {template} not in the formatted_row",
                "formatted_row": answer["formatted_row"]
            }
        target_string = answer["formatted_row"].replace(template, answer["data"])
        try:
            pos = self._extract_row_number(target_string)
        except TypeError:
            return {
                "message": "ERROR: can't extract row number",
                "formatted_row": target_string
            }
        true_string = self.trade_description_rows[pos]
        if true_string != target_string:
            return {
                "message": "ERROR: the rows are not the same",
                "input_row": true_string,
                "extracted_row": target_string,
                "formatted_row": answer["formatted_row"],
            }
        return dict()

    def check_field(self, field: str, answer: Union[List, Dict]) -> List:
        if (isinstance(answer, Dict) and self.field_freq[field] == "multiple") or \
                (isinstance(answer, List) and self.field_freq[field] == "single"):
            return [{
                "message": "Frequency of the answer is incorrect",
                "freq": self.field_freq[field],
                "answer_type": str(type(answer))
            }]
        if isinstance(answer, Dict):
            error_message = self.check_field_piece(field, answer)
            if error_message:
                return [error_message]
        else:
            error_messages = []
            for answer_piece in answer:
                error_message = self.check_field_piece(field, answer_piece)
                if error_message:
                    error_messages.append(error_message)
            return error_messages

    def check_answer(self, json_answer: Dict) -> Dict:
        status = dict()
        for field, field_answer in json_answer.items():
            error_messages = self.check_field(field, field_answer)
            if error_messages:
                status[field] = {
                    "error_messages": error_messages,
                    "status": "BAD"
                }
            else:
                status[field] = {
                    "status": "OK"
                }
        return status
