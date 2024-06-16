# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.storage.attrs import data_class, data_field
from cl.runtime.storage.key import Key


@data_class
class UserKey(Key):
    """Key for WhitelistedUser class"""

    username: str = data_field()
