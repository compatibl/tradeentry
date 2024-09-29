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
import uuid
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from cl.runtime import Context
from cl.runtime.context.process_context import ProcessContext
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.log.log_entry import LogEntry
from cl.runtime.log.log_entry_level_enum import LogEntryLevelEnum
from cl.runtime.primitive.datetime_util import DatetimeUtil
from cl.runtime.routers.app import app_router
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
from stubs.cl.runtime.config.stub_runtime_config import StubRuntimeConfig  # TODO: Remove after refactoring

# Server
server_app = FastAPI()


# Universal exception handler function
async def handle_exception(request, exc, log_level):

    # Get context logger using request URL as name
    logger = Context.current().get_logger(str(request.url))

    # Log the exception
    logger.error(repr(exc))

    # Output traceback
    traceback.print_exception(exc)

    # Save log entry to the database
    entry = LogEntry(
        id=str(uuid.uuid4()),
        message=str(exc),
        level=log_level,
        timestamp=DatetimeUtil.to_iso_int(DatetimeUtil.now()),
    )
    Context.current().save_one(entry)

    # Return 500 response to avoid exception handler multiple calls
    return Response("Internal Server Error", status_code=500)


# Add RuntimeError exception handler
@server_app.exception_handler(RuntimeError)
async def http_exception_handler(request, exc):
    return await handle_exception(request, exc, log_level=LogEntryLevelEnum.ERROR)


# Add Warning exception handler
@server_app.exception_handler(Warning)
async def http_warning_handler(request, exc):
    return await handle_exception(request, exc, log_level=LogEntryLevelEnum.WARNING)


# Add UserError exception handler
@server_app.exception_handler(UserError)
async def http_user_error_handler(request, exc):
    return await handle_exception(request, exc, log_level=LogEntryLevelEnum.USER_ERROR)


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
server_app.include_router(app_router.router, prefix="", tags=["App"])
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
        log_dir = os.path.join(Settings.get_project_root(), "logs")  # TODO: Make unique
        celery_start_queue(log_dir=log_dir)

        # TODO: Temporary workaround before full configuration workflow is supported
        config = StubRuntimeConfig()
        config.config_id = "Stub Runtime Config"
        config.run_configure()

        # Preload data
        PreloadSettings.instance().preload()

        # Find wwwroot directory relative to the location of __main__ rather than project root
        wwwroot_dir = Settings.get_static_files_path()

        if os.path.exists(wwwroot_dir):
            # Launch UI if ui_path is found
            server_app.mount("/", StaticFiles(directory=wwwroot_dir, html=True))
        else:
            print(f"UI directory {wwwroot_dir} not found, starting REST API only.")

        # Run Uvicorn using hostname and port specified by Dynaconf
        api_settings = ApiSettings.instance()
        uvicorn.run(server_app, host=api_settings.host_name, port=api_settings.port)
