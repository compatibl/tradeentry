# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from dataclasses import dataclass
from typing import Tuple
from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield
from cl.runtime.records.dataclasses.dataclass_key_mixin import DataclassKeyMixin
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.schema.type_decl_key import TypeDeclKey


@dataclass(slots=True)
class UiTypeStateKey(DataclassKeyMixin):
    """Defines some default settings for a type."""

    type_: TypeDeclKey = datafield()
    """Type reference."""

    user: UserKey | None = datafield()
    """A user the app state is applied for."""

    def get_generic_key(self) -> Tuple:
        return UiTypeStateKey, self.type_, self.user
