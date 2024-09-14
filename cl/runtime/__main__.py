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
import uvicorn
from cl.runtime.context.process_context import ProcessContext
from cl.runtime.routers.auth import auth_router
from cl.runtime.routers.entity import entity_router
from cl.runtime.routers.health import health_router
from cl.runtime.routers.schema import schema_router
from cl.runtime.routers.storage import storage_router
from cl.runtime.routers.tasks import tasks_router
from cl.runtime.settings.api_settings import ApiSettings
from cl.runtime.settings.preload_settings import PreloadSettings
from cl.runtime.settings.settings import Settings
from cl.runtime.tasks.celery.celery_queue import celery_delete_existing_tasks
from cl.runtime.tasks.celery.celery_queue import celery_start_queue
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from stubs.cl.runtime.config.stub_runtime_config import StubRuntimeConfig  # TODO: Remove after refactoring

# Server
server_app = FastAPI()

# Get Runtime settings from Dynaconf
api_settings = ApiSettings.instance()

# Permit origins based on either hostname or host IP
origins = [
    f"{api_settings.host_name}:{api_settings.port}",
    f"{api_settings.host_ip}:{api_settings.port}",
]

server_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Specify allowed HTTP methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # Specify allowed headers, e.g., ["Content-Type", "Authorization"]
)

# Routers
server_app.include_router(health_router.router, prefix="", tags=["Health Check"])
server_app.include_router(auth_router.router, prefix="/auth", tags=["Authorization"])
server_app.include_router(schema_router.router, prefix="/schema", tags=["Schema"])
server_app.include_router(storage_router.router, prefix="/storage", tags=["Storage"])
server_app.include_router(entity_router.router, prefix="/entity", tags=["Entity"])
server_app.include_router(tasks_router.router, prefix="/tasks", tags=["Tasks"])

if __name__ == "__main__":
    with ProcessContext():
        # TODO: This only works for the Mongo celery backend
        celery_delete_existing_tasks()

        # Start Celery workers (will exit when the current process exits)
        celery_start_queue()

        # TODO: Temporary workaround before full configuration workflow is supported
        config = StubRuntimeConfig()
        config.config_id = "Stub Runtime Config"
        config.configure()

        # Preload data
        PreloadSettings.instance().preload()

        # TODO: Make it possible to override wwwroot directory location in settings
        project_root = Settings.get_project_root()
        wwwroot_dir = os.path.join(project_root, "wwwroot")

        if os.path.exists(wwwroot_dir):
            # Launch UI if ui_path is found
            server_app.mount("/", StaticFiles(directory=wwwroot_dir, html=True))
            print(f"Starting UI")
        else:
            print(f"UI directory {wwwroot_dir} not found, starting REST API only.")

        # Run Uvicorn using hostname and port specified by Dynaconf
        api_settings = ApiSettings.instance()
        uvicorn.run(server_app, host=api_settings.host_name, port=api_settings.port)
