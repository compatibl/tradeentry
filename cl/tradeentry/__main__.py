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

import os
import traceback

import uvicorn
from starlette.staticfiles import StaticFiles

from cl.runtime.__main__ import server_app
from cl.runtime.context.process_context import ProcessContext
from cl.runtime.settings.api_settings import ApiSettings
from cl.runtime.settings.preload_settings import PreloadSettings
from cl.runtime.settings.settings import Settings
from cl.runtime.tasks.celery.celery_queue import celery_delete_existing_tasks
from cl.runtime.tasks.celery.celery_queue import celery_start_queue
from stubs.cl.runtime.config.stub_runtime_config import StubRuntimeConfig  # TODO: Remove after refactoring

if __name__ == "__main__":
    with ProcessContext():
        # TODO: This only works for the Mongo celery backend
        celery_delete_existing_tasks()

        # Start Celery workers (will exit when the current process exits)
        celery_start_queue()

        # Preload data
        PreloadSettings.instance().preload()

        # Find wwwroot directory relative to the location of __main__ rather than project root
        wwwroot_dir = Settings.get_static_files_path()

        if os.path.exists(wwwroot_dir):
            # Launch UI if ui_path is found
            server_app.mount("/", StaticFiles(directory=wwwroot_dir, html=True))
            print(f"Starting UI")
        else:
            print(f"UI directory {wwwroot_dir} not found, starting REST API only.")

        # Run Uvicorn using hostname and port specified by Dynaconf
        api_settings = ApiSettings.instance()
        uvicorn.run(server_app, host=api_settings.host_name, port=api_settings.port)
