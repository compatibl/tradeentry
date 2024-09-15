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

from __future__ import annotations
import ast
import dataclasses
import inspect
from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
from itertools import tee
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Set
from typing import Type
from typing import get_type_hints
from inflection import camelize
from inflection import titleize
from memoization import cached
from typing_extensions import Self
from cl.runtime.records.dataclasses_extensions import missing
from cl.runtime.records.key_util import KeyUtil
from cl.runtime.records.record_mixin import RecordMixin
from cl.runtime.schema.element_decl import ElementDecl
from cl.runtime.schema.field_decl import FieldDecl
from cl.runtime.schema.handler_declare_block_decl import HandlerDeclareBlockDecl
from cl.runtime.schema.module_decl_key import ModuleDeclKey
from cl.runtime.schema.type_decl_key import TypeDeclKey
from cl.runtime.schema.type_kind import TypeKind

DisplayKindLiteral = Literal["Basic", "Singleton", "Dashboard"]


def pascalize(s: str) -> str:
    """Split into dot-delimited tokens, pascalize each token, then concatenate."""
    tokens = s.split(".")
    tokens = [camelize(token, uppercase_first_letter=True) for token in tokens]
    result = ".".join(tokens)
    return result


def to_type_decl_dict(node: Dict[str, Any] | List[Dict[str, Any]] | str) -> Dict[str, Any] | List[Dict[str, Any]] | str:
    """Recursively apply type declaration dictionary conventions to the argument dictionary."""

    if isinstance(node, dict):
        # For type declarations only, skip nodes that have the value of None or False
        # Remove suffix _ from field names if present
        # pascalized_values = {k: (pascalize(v) if k in ['module_name', 'name'] else v) for k, v in node.items()}
        # Searching for the name of given type declaration
        result: Dict[str, Any] = {}
        if (_t := get_name_of_type_decl_dict(node)) is not None:
            result["_t"] = pascalize(_t)
        result.update(
            {
                (pascalize(k.removesuffix("_")) if k != "_t" else k): to_type_decl_dict(v)
                for k, v in node.items()
                if v not in [None, False]
            }
        )
        return result
    elif isinstance(node, list):
        # For type declarations only, skip nodes that have the value of None or False
        return [to_type_decl_dict(v) for v in node if v not in [None, False]]
    elif isinstance(node, tuple):
        # The first element of key node tuple is type, the remaining elements are primary key fields
        # Remove suffix _ from field names if present
        key_field_names = node[0].get_key_fields()
        key_field_values = [to_type_decl_dict(v) for v in node[1:]]
        return {pascalize(k.removesuffix("_")): v for k, v in zip(key_field_names, key_field_values)}
    elif isinstance(node, str):
        return pascalize(node)
    else:
        return node


def for_type_key_maker(
    cls,
    record_type: Type,
    *,
    dependencies: Set[Type] | None = None,
    skip_fields: bool = False,
    skip_handlers: bool = False,
) -> str:
    """Custom key marker for 'for_type' class method."""
    # TODO: Replace by lambda if skip_fields parameter is removed
    return f"{record_type.__module__}.{record_type.__name__}.{dependencies.__hash__}{skip_fields}{skip_handlers}"


def get_name_of_type_decl_dict(dict_: Dict[str, Dict]) -> Optional[str]:
    """Search for the type name in the given dict and return in format {module}.{name} ."""

    # Element fields contain "key_" in case of key-field or "data" section in case of data-field
    key_field = dict_.get("key_", None)
    data_field = dict_.get("data", None)
    name_field = "name"
    module_field = "module"
    module_name_field = "module_name"

    module = None
    name = None

    if key_field is not None and name_field in key_field:
        module = key_field.get(module_field, {}).get(module_name_field, None)
        name = key_field[name_field]
    elif data_field is not None and name_field in data_field:
        module = data_field.get(module_field, {}).get(module_name_field, None)
        name = data_field[name_field]
    # Name of the whole type is contained in "name" field. But type decl cannot contain only "name" and "module" fields
    elif (name_ := dict_.get(name_field, None)) is not None and module_field in dict_:
        if len(dict_) > 2:
            name = name_

    type_name = f"{module}.{name}" if module is not None else name
    return type_name


@dataclass(slots=True, kw_only=True)
class TypeDecl(TypeDeclKey, RecordMixin[TypeDeclKey]):
    """Provides information about a class, its fields, and its methods."""

    label: str | None = missing()
    """Type label."""

    comment: str | None = missing()
    """Type comment. Contains additional information."""

    kind: TypeKind | None = missing()
    """Type kind."""

    display_kind: DisplayKindLiteral = missing()  # TODO: Make optional, treat None as Basic
    """Display kind."""

    inherit: TypeDeclKey | None = missing()
    """Parent type reference."""

    declare: HandlerDeclareBlockDecl | None = missing()  # TODO: Flatten or use block for abstract flag
    """Handler declaration block."""

    elements: List[ElementDecl] | None = missing()  # TODO: Consider renaming to fields
    """Element declaration block."""

    keys: List[str] | None = missing()
    """Array of key element names (specify in base class only)."""

    # TODO: Consider moving to Table class
    # indexes: List[TypeIndexDecl] | None = missing()
    """Defines indexes for the type."""

    immutable: bool | None = missing()
    """Immutable flag."""

    permanent: bool | None = missing()
    """When the record is saved, also save it permanently."""

    def get_key(self) -> TypeDeclKey:
        return TypeDeclKey(module=self.module, name=self.name)

    def to_type_decl_dict(self) -> Dict[str, Any]:
        """Convert to dictionary using type declaration conventions."""

        # Convert to standard dictionary format
        standard_dict = asdict(self)

        # Apply type declaration dictionary conventions
        result = to_type_decl_dict(standard_dict)
        return result

    @classmethod
    def for_key(cls, key: TypeDeclKey) -> Self:
        """Create or return cached object for the specified type declaration key."""
        class_path = f"{key.module.module_name}.{key.name}"
        return cls.for_class_path(class_path)

    @classmethod
    def for_class_path(cls, class_path: str) -> Self:
        """Create or return cached object for the specified class path in module.ClassName format."""
        raise NotImplementedError()

    @classmethod
    @cached(custom_key_maker=for_type_key_maker)
    def for_type(
        cls,
        record_type: Type,
        *,
        dependencies: Set[Type] | None = None,
        skip_fields: bool = False,
        skip_handlers: bool = False,
    ) -> Self:
        """
        Create or return cached object for the specified record type.

        Args:
            record_type: Type of the record for which the declaration is created
            dependencies: Set of types used in field or methods of the specified type, populated only if not None
            skip_fields: Use this flag to skip fields generation when the method is invoked from a derived class
            skip_handlers: Use this flag to skip handlers generation when the method is invoked internal methods
        """

        if issubclass(record_type, Enum):
            raise RuntimeError(f"Cannot create TypeDecl for class {record_type.__name__} because it is an enum.")
        if issubclass(record_type, tuple):
            raise RuntimeError(f"Cannot create TypeDecl for class {record_type.__name__} because it is a tuple.")

        # Create instance of the final type
        result = cls()

        result.module = ModuleDeclKey(module_name=record_type.__module__)
        result.name = record_type.__name__
        result.label = titleize(result.name)  # TODO: Add override from settings
        result.comment = record_type.__doc__

        # Set type kind by detecting the presence of 'get_key' method to indicate a record vs. an element
        is_record = hasattr(record_type, "get_key")
        is_abstract = hasattr(record_type, "__abstractmethods__") and bool(record_type.__abstractmethods__)
        if is_record:
            result.kind = "abstract" if is_abstract else None
        else:
            result.kind = "abstract_element" if is_abstract else "element"

        # Set display kind
        result.display_kind = "Basic"  # TODO: Remove Basic after display_kind is made optional

        # Set parent class as the first class in MRO that is not self and does not have Mixin suffix
        for parent_type in record_type.__mro__:
            # TODO: Refactor to make it work not only for dataclasses
            if (
                parent_type is not record_type
                and not parent_type.__name__.endswith("Mixin")
                and not parent_type.__name__.endswith("Key")
                and dataclasses.is_dataclass(parent_type)
            ):
                parent_type_decl = cls.for_type(parent_type, dependencies=dependencies)
                result.inherit = parent_type_decl.get_key()

                # Add to dependencies
                if dependencies is not None:
                    dependencies.add(parent_type)

        # Get type public methods
        if not skip_handlers:
            handlers_block = HandlerDeclareBlockDecl.get_type_methods(record_type)
            if handlers_block.handlers:
                result.declare = handlers_block

        # Get key fields by parsing the source of 'get_key' method
        result.keys = KeyUtil.get_key_fields(record_type)  # TODO: Use slots of key type when present?

        # Use this flag to skip fields generation when the method is invoked from a derived class
        if not skip_fields:
            # Get type hints to resolve ForwardRefs
            type_hints = get_type_hints(record_type)

            # Dictionary of member comments (docstrings), currently requires source parsing due Python limitations
            member_comments = cls.get_member_comments(record_type)

            # Add an element for each type hint
            result.elements = []
            for field_name, field_type in type_hints.items():
                # Field comment (docstring)
                field_comment = member_comments.get(field_name, None)

                # Get the rest of the data from the field itself
                field_decl = FieldDecl.create(
                    record_type, field_name, field_type, field_comment, dependencies=dependencies
                )

                # Convert to element and add
                element_decl = ElementDecl.create(field_decl)
                result.elements.append(element_decl)

        return result

    @classmethod
    @cached
    def get_member_comments(cls, record_type: type) -> Dict[str, str]:
        """Extract class member comments."""

        # Include comments from key class fields for base
        # TODO: Revise approach to key fields
        if len(record_type.__mro__) > 1 and record_type.__mro__[1].__name__.endswith("Key"):
            comments = cls.get_member_comments(record_type.__mro__[1])
        else:
            comments = dict()

        ast_tree = ast.parse(inspect.getsource(record_type))

        for i, j in cls.by_pair(ast.iter_child_nodes(ast_tree.body[0])):
            if isinstance(i, ast.AnnAssign):
                target_node = i.target
            elif isinstance(i, ast.Assign):
                target_node = i.targets[0]
            else:
                continue

            if not isinstance(target_node, ast.Name):
                continue

            name: str = target_node.id
            # TODO: ast.Str is replaced by ast.Constant in Python 3.8, update
            if isinstance(j, ast.Expr) and isinstance(j.value, ast.Str):
                comments[name] = inspect.cleandoc(j.value.s)

        return comments

    @classmethod
    def by_pair(cls, iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)
