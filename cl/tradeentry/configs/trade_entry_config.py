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

from dataclasses import dataclass
from cl.runtime.backend.core.base_type_info import BaseTypeInfo
from cl.runtime.backend.core.tab_info import TabInfo
from cl.runtime.backend.core.ui_app_state import UiAppState
from cl.runtime.backend.core.user_key import UserKey
from cl.runtime.configs.config import Config
from cl.runtime.context.context import Context


@dataclass(slots=True, kw_only=True)
class TradeEntryConfig(Config):
    """Configure the initial set of records for TradeEntry."""

    def run_configure(self) -> None:

        # Save UiAppState instance
        context = Context.current()
        context.save_one(
            UiAppState(
                user=UserKey(username="root"),  # TODO: Avoid reliance on the default user
                opened_tabs=[
                    TabInfo(
                        type=BaseTypeInfo(
                            name="Entry",
                            module="Entry",
                            label="Entry",
                        ),
                    ),
                ],
            ),
        )
