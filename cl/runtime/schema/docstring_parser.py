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
from typing import Optional
from typing import Pattern

# Regexp for docstring parsing
__parameters_re: Pattern = re.compile(r"Parameters\s+----------")
__returns_re: Pattern = re.compile(r"Returns\s+-------")


class MethodDocstringParameter:  # TODO: Move to a separate directory with other helper classes
    """Represents method argument docstring."""

    name: str = None
    """ Argument name. """

    type_: str = None
    """ Argument type. """

    optional: bool = None
    """ Argument is optional. """

    comment: str = None
    """ Argument comment. """

    meta: Dict[str, str] = None
    """ Argument meta information. """


class MethodDocstring:
    """Represents method docstring."""

    comment: str = None
    """ Method comment. """

    parameters: Dict[str, MethodDocstringParameter] = None
    """ Method parameters. """

    returns: MethodDocstringParameter = None
    """ Method returns. """

    def __init__(self):
        """Initialize an instance of MethodDocstring."""
        self.parameters = dict()


class EnumItemDocstring:
    """Represents enum item docstring."""

    comment: str = None
    """Item comment."""

    label: str = None
    """ Item label. """


def _parse_param_metadata(line: str) -> Optional[Dict[str, str]]:
    """Parse param line in format 'param_name : param_type[, ..]'."""

    param_options = line.split(",")

    # Parse first item in format '[name : ]type'
    name_type = [x.strip() for x in param_options[0].split(" : ")]

    if len(name_type) > 2:
        return None

    result = dict()
    if len(name_type) == 2:
        result["_name"] = name_type[0]
        result["_type"] = name_type[1]
    else:
        result["_type"] = name_type[0]

    # Parse param options in format 'key[=val]'
    for opt in param_options[1:]:
        key_val = [x.strip() for x in opt.split("=")]

        if len(key_val) > 2:
            return None
        elif len(key_val) == 2:
            result[key_val[0]] = key_val[1]
        else:
            result[key_val[0]] = None

    return result


def _parse_method_docstring_param(param_line: str) -> MethodDocstringParameter:
    """Parse docstring parameter line."""

    param_meta = _parse_param_metadata(param_line)

    result = MethodDocstringParameter()
    result.name = param_meta.pop("_name", None)
    result.type_ = param_meta.pop("_type", None)
    result.meta = param_meta

    if "optional" in param_meta:
        param_opt = param_meta["optional"]
        if param_opt is None or param_opt == "True":
            result.optional = True

    return result


def _parse_method_docstring_returns(returns_block: str, result: MethodDocstring):
    """Extract return docstring."""

    returns_lines = [x for x in returns_block.splitlines() if len(x) != 0 and not x.isspace()]

    if len(returns_lines) == 0:
        return

    returns_doc = _parse_method_docstring_param(returns_lines[0])

    # Extract returns comment
    if len(returns_lines) > 1:
        returns_doc.comment = returns_lines[1].strip()

    result.returns = returns_doc


def _parse_method_docstring_parameters(parameters_block: str, result: MethodDocstring):
    """Extract parameters docstring."""

    parameters_lines = [x for x in parameters_block.splitlines() if len(x) != 0 and not x.isspace()]

    # Parse parameters, check i and i+1 lines
    i = 0
    while i < len(parameters_lines):
        # Find the line in format 'param_name : param_type[, ..]'
        param_doc = _parse_method_docstring_param(parameters_lines[i])

        if param_doc.name is not None:
            result.parameters[param_doc.name] = param_doc

            # Go to next line
            i += 1
            if i >= len(parameters_lines):
                break

            # Check if next line is not param comment
            param_type_next = parameters_lines[i].split(" : ")
            if len(param_type_next) >= 2:
                continue

            # Extract param comment
            param_comment = parameters_lines[i].strip()
            param_doc.comment = param_comment

        # Go to next line
        i += 1


def parse_method_docstring(method_doc: str | None) -> MethodDocstring:
    """Parse method docstring and extracts comments."""

    result = MethodDocstring()

    if method_doc is None:
        return result

    # Extract returns block
    returns_start = __returns_re.search(method_doc)
    if returns_start is not None:
        returns_block = method_doc[returns_start.end() :]
        method_doc = method_doc[: returns_start.start()]

        _parse_method_docstring_returns(returns_block, result)

    # Extract parameters block
    parameters_start = __parameters_re.search(method_doc)
    if parameters_start is not None:
        parameters_block = method_doc[parameters_start.end() :]
        method_doc = method_doc[: parameters_start.start()]

        _parse_method_docstring_parameters(parameters_block, result)

    # Extract comment
    comment = method_doc.strip()
    if len(comment) != 0:
        result.comment = comment

    return result


def parse_enum_items_definition(enum_item_docstring: str, enum_type_name: str, enum_item: str) -> EnumItemDocstring:
    """Parse enum label in format 'Item Label = label name.(not case sensitive)."""

    result = EnumItemDocstring()
    label_exist = re.compile(r"item\s*label\s*=", flags=re.I).search(enum_item_docstring)

    if label_exist:
        result.comment = enum_item_docstring[: label_exist.start()].strip()
        correct_setup_label_structure = len(enum_item_docstring[label_exist.start() :].split("=")) == 2

        if not correct_setup_label_structure:
            raise RuntimeError(f"Invalid {enum_type_name} item label definition in the item {enum_item}.")

        result.label = enum_item_docstring[label_exist.start() :].split("=")[1].strip()
    else:
        result.comment = enum_item_docstring.strip()

    return result
