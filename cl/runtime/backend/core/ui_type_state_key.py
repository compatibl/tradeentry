# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.records.dataclasses_extensions import field, missing
from cl.runtime.records.key_mixin import KeyMixin
from cl.runtime.schema.type_decl_key import TypeDeclKey
from dataclasses import dataclass
from typing import Type


@dataclass(slots=True, kw_only=True)
class UiTypeStateKey(KeyMixin):
    """Defines some default settings for a type."""

    type_: TypeDeclKey = missing()
    """Type reference."""

    user: UserKey | None = missing()
    """A user the app state is applied for."""

    def get_key_type(self) -> Type:
        return UiTypeStateKey
