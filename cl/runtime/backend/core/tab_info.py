# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.backend.core.base_type_info import BaseTypeInfo
from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield
from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True, kw_only=True)
class TabInfo:
    """Tab info."""

    type_: BaseTypeInfo = datafield()
    """Type."""

    # key: Tuple | None = datafield()  # TODO: Add generic key support
    """Key."""
