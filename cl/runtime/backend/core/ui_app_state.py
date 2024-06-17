# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from typing import List, Optional

from cl.runtime.backend.core.app_theme import AppTheme
from cl.runtime.backend.core.tab_info import TabInfo
from cl.runtime.backend.core.ui_app_state_key import UiAppStateKey, UiAppStateTable
from cl.runtime.backend.core.user_key import UserKey
from dataclasses import dataclass
from cl.runtime.records.dataclasses.dataclass_mixin import datafield, DataclassMixin


@dataclass(slots=True, kw_only=True)
class UiAppState(DataclassMixin):
    """UiAppState."""

    user: UserKey = datafield()
    """A user the app state is applied for."""

    opened_tabs: List[TabInfo] | None = datafield()
    """Information about opened tabs."""

    active_tab_index: int | None = datafield()
    """Index of active opened tab."""

    backend_version: str | None = datafield()
    """DEPRECATED. Use versions instead."""

    application_name: str | None = datafield()
    """Application name."""

    read_only: bool | None = datafield()
    """Flag indicating that UI is read-only."""

    application_theme: AppTheme | None = datafield()
    """Application theme (dark, light, etc.)."""

    def get_key(self) -> UiAppStateKey:
        return UiAppStateTable, self.user

    @staticmethod
    def get_current_user_app_theme() -> AppTheme | None:
        """Get current user app theme."""
        return "Light"  # TODO: Use settings

