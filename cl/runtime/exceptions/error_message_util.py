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

from typing import Type, Any
from cl.runtime.primitive.case_util import CaseUtil
from cl.runtime.primitive.string_util import StringUtil


class ErrorMessageUtil:
    """Helper class for formatting error messages."""

    @classmethod
    def short_value(
            cls,
            value: Any,
            *,
            value_name: str | None = None,
            method_name: str | None = None,
            data_type: Type | str | None = None,
    ) -> str:
        """
        Description of a variable, field or parameter value followed by space suitable for short values (value first).

        Args:
            value: The value for which the error is reported
            value_name: Variable, field or parameter name for formatting the error message (optional)
            method_name: Method or function name for formatting the error message (optional)
            data_type: Class type or name for formatting the error message (optional)
        """
        if method_name is not None:
            of_what = cls.of_param(param_name=value_name, method_name=method_name, data_type=data_type)
        elif data_type is not None:
            of_what = cls.of_field(field_name=value_name, data_type=data_type)
        elif value_name is not None:
            if CaseUtil.is_snake_case(value_name):
                value_name = CaseUtil.snake_to_pascal_case(value_name)
            of_what = f"of {value_name} "
        else:
            of_what = ""

        if value is not None:
            return f"The value '{str(value)}' {of_what}"
        else:
            return f"An empty value {of_what}"

    @classmethod
    def of_field(
            cls,
            *,
            field_name: str | None = None,
            data_type: Type | str | None = None,
    ) -> str:
        """
        Descriptive field name followed by space.

        Args:
            field_name: Parameter or field name for formatting the error message (optional)
            data_type: Class type or name for formatting the error message (optional)
        """
        # Convert field name
        if not StringUtil.is_empty(field_name):
            if CaseUtil.is_snake_case(field_name):
                field_name = CaseUtil.snake_to_pascal_case(field_name)
            field_str = f"of field {field_name} "
        elif data_type is not None:
            field_str = "of a field "
        else:
            field_str = ""

        # Convert type
        if data_type is not None:
            data_type = data_type.__name__ if isinstance(data_type, type) else str(data_type)
        if not StringUtil.is_empty(data_type):
            record_str = f"in {data_type} "
        else:
            record_str = ""

        # Create the message
        result = f"{field_str}{record_str}"
        return result

    @classmethod
    def of_param(
            cls,
            *,
            param_name: str | None = None,
            method_name: str | None = None,
            data_type: Type | str | None = None,
    ) -> str:
        """
        Descriptive field name followed by space or empty string if details are not provided.

        Args:
            param_name: Parameter name for formatting the error message (optional)
            method_name: Method or function name for formatting the error message (optional)
            data_type: Class type or name for formatting the error message (optional)
        """
        # Convert field name
        if not StringUtil.is_empty(param_name):
            if CaseUtil.is_snake_case(param_name):
                param_name = CaseUtil.snake_to_pascal_case(param_name)
            field_str = f"of parameter {param_name} "
        elif method_name is not None:
            field_str = "of a parameter "
        else:
            return ""
            
        # Convert class name
        if data_type is not None:
            data_type = data_type.__name__ if isinstance(data_type, type) else str(data_type)

        # Convert method name
        if not StringUtil.is_empty(method_name):
            if CaseUtil.is_snake_case(method_name):
                method_name = CaseUtil.snake_to_pascal_case(method_name)
            if StringUtil.is_empty(data_type):
                return f"{field_str}in function {method_name} "
            else:
                return f"{field_str}in method {method_name} of {data_type} "
        else:
            return field_str
