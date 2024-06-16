# Copyright (C) 2003-present CompatibL. All rights reserved.
#
# This file contains valuable trade secrets and may be copied, stored, used,
# or distributed only in compliance with the terms of a written commercial
# license from CompatibL and with the inclusion of this copyright notice.

from typing import List, Optional

from cl.runtime.backend.core.app_theme import AppTheme
from cl.runtime.backend.core.tab_info import TabInfo
from cl.runtime.backend.core.ui_app_state_key import UiAppStateKey
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.storage.attrs import data_class, data_field
from cl.runtime.storage.context import Context


@data_class
class UiAppState(UiAppStateKey):
    """UiAppState."""

    opened_tabs: Optional[List[TabInfo]] = data_field()
    """Information about opened tabs."""

    active_tab_index: Optional[int] = data_field()
    """Index of active opened tab."""

    versions: Optional[dict] = data_field()
    """Component versions."""

    backend_version: Optional[str] = data_field()
    """DEPRECATED. Use versions instead."""

    application_name: Optional[str] = data_field()
    """Application name."""

    read_only: Optional[bool] = data_field()
    """Flag indicating that UI is read-only."""

    application_theme: Optional[AppTheme] = data_field()
    """Application theme (dark, light, etc.)."""

    @staticmethod
    def get_current_user_app_theme() -> AppTheme:
        """Get current user app theme."""
        username = Context.current().user
        current_app_state: UiAppState = Context.current().load_one(
            key=UiAppStateKey(user=UserKey(username=username)),
            ignore_not_found=True,
        )
        if current_app_state is not None and current_app_state.application_theme is not None:
            return current_app_state.application_theme

        default_app_state: UiAppState = Context.current().load_one(
            key=UiAppStateKey(user=None),
            ignore_not_found=True,
        )
        if default_app_state is not None and default_app_state.application_theme is not None:
            return default_app_state.application_theme

        return AppTheme.Light
