# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from dataclasses import dataclass
from cl.runtime.records.dataclasses.dataclass_data_mixin import datafield


@dataclass(slots=True, kw_only=True)
class BaseTypeInfo:
    """Base type info."""

    name: str = datafield()
    """Name of type."""

    module: str = datafield()
    """Module of type."""

    label: str = datafield()
    """Label of type."""
