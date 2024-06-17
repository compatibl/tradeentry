# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.backend.core.base_type_info import BaseTypeInfo
from dataclasses import dataclass
from cl.runtime.records.dataclasses.dataclass_mixin import datafield
from cl.runtime.records.generic_key import GenericKey


@dataclass(slots=True, kw_only=True)
class TabInfo:
    """Tab info."""

    type_: BaseTypeInfo = datafield()
    """Type."""

    key: GenericKey | None = datafield()
    """Key."""
