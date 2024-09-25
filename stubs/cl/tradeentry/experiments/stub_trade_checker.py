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
from typing import Dict
from typing import List
from typing import Union


class StubFormattedStringChecker:
    def __init__(self, trade_description: str, field_description: List[Dict]):
        self.trade_description_rows = self._get_rows_from_numbered_text(trade_description)
        self.field_freq = {field["name"]: field["freq"] for field in field_description}

    @staticmethod
    def _extract_row_number(row: str) -> int:
        try:
            row_num = int(row[: row.index(":")])
        except:
            raise TypeError(f"Can not extract row number for row {row}")
        return row_num

    @staticmethod
    def _get_rows_from_numbered_text(text: str) -> Dict:
        rows = text.split("\n")
        answer = dict()
        for row in rows:
            row_num = StubFormattedStringChecker._extract_row_number(row)
            answer[row_num] = row
        return answer

    def check_field_piece(self, field: str, answer: Dict) -> Dict:

        # Check if data or formatted_row are missing in the answer
        if "data" not in answer or "formatted_row" not in answer:
            return {"message": "ERROR: Missing required fields 'data' or 'formatted_row' in answer", "answer": answer}

        # Check if data is empty
        if not answer.get("data"):
            return {}

        # Check if the data is of string type
        if not isinstance(answer["data"], str):
            return {
                "message": "ERROR: answer data is not string type",
                "type": str(type(answer["data"])),
                "data": answer["data"],
            }

        # Check if field in the formatted_row
        template = "{" + field + "}"
        if template not in answer["formatted_row"]:
            return {"message": f"ERROR: {template} not in the formatted_row", "formatted_row": answer["formatted_row"]}

        # Replace the field with the actual data
        extracted_string = answer["formatted_row"].replace(template, answer["data"])

        # Attempt to extract the row number
        try:
            pos = self._extract_row_number(extracted_string)
        except TypeError:
            return {"message": "ERROR: can't extract row number", "extracted_row": extracted_string}

        # Compare the resulting string with the expected input string
        input_string = self.trade_description_rows[pos]
        if input_string != extracted_string:
            return {
                "message": "ERROR: the rows are not the same",
                "input_row": input_string,
                "extracted_row": extracted_string,
                "formatted_row": answer["formatted_row"],
            }
        return {}

    def check_field(self, field: str, answer: Union[List, Dict]) -> List:

        if (isinstance(answer, Dict) and self.field_freq[field] == "multiple") or (
            isinstance(answer, List) and self.field_freq[field] == "single"
        ):
            return [
                {
                    "message": "Frequency of the answer is incorrect",
                    "freq": self.field_freq[field],
                    "answer_type": str(type(answer)),
                }
            ]

        if isinstance(answer, Dict):
            error_message = self.check_field_piece(field, answer)
            if error_message:
                return [error_message]
        elif isinstance(answer, List):
            error_messages = []
            for answer_piece in answer:
                error_message = self.check_field_piece(field, answer_piece)
                if error_message:
                    error_messages.append(error_message)
            return error_messages
        else:
            return [{"message": f"ERROR: answer is not Dict or List type", "type": str(type(answer)), "answer": answer}]

    def check_answer(self, json_answer: Dict) -> Dict:
        status = dict()
        for field, field_answer in json_answer.items():
            error_messages = self.check_field(field, field_answer)
            if error_messages:
                status[field] = {"error_messages": error_messages, "status": "BAD"}
            else:
                status[field] = {"status": "OK"}
        return status
