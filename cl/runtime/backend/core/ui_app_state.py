# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from cl.runtime.backend.core.app_theme import AppTheme
from cl.runtime.backend.core.tab_info import TabInfo
from cl.runtime.backend.core.ui_app_state_key import UiAppStateKey
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.records.dataclasses_extensions import field
from cl.runtime.records.record_mixin import RecordMixin
from dataclasses import dataclass
from typing import List
from typing import Optional


@dataclass(slots=True, kw_only=True)
class UiAppState(UiAppStateKey, RecordMixin[UiAppStateKey]):
    """UiAppState."""

    opened_tabs: List[TabInfo] | None = field()
    """Information about opened tabs."""

    active_tab_index: int | None = field()
    """Index of active opened tab."""

    backend_version: str | None = field()
    """DEPRECATED. Use versions instead."""

    application_name: str | None = field()
    """Application name."""

    read_only: bool | None = field()
    """Flag indicating that UI is read-only."""

    application_theme: str | None = field()  # TODO: Replace by AppTheme
    """Application theme (dark, light, etc.)."""

    def get_key(self) -> UiAppStateKey:
        return UiAppStateKey(user=self.user)

    @staticmethod
    def get_current_user_app_theme() -> AppTheme | None:
        """Get current user app theme."""
        return "Light"  # TODO: Use settings
