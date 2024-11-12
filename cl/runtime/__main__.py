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
import webbrowser
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from cl.runtime import Context
from cl.runtime.context.process_context import ProcessContext
from cl.runtime.log.exceptions.user_error import UserError
from cl.runtime.log.log_entry import LogEntry
from cl.runtime.log.log_entry_level_enum import LogEntryLevelEnum
from cl.runtime.log.user_log_entry import UserLogEntry
from cl.runtime.routers.app import app_router
from cl.runtime.routers.auth import auth_router
from cl.runtime.routers.context_middleware import ContextMiddleware
from cl.runtime.routers.entity import entity_router
from cl.runtime.routers.health import health_router
from cl.runtime.routers.schema import schema_router
from cl.runtime.routers.storage import storage_router
from cl.runtime.routers.tasks import tasks_router
from cl.runtime.settings.api_settings import ApiSettings
from cl.runtime.settings.preload_settings import PreloadSettings
from cl.runtime.settings.project_settings import ProjectSettings
from cl.runtime.tasks.celery.celery_queue import celery_delete_existing_tasks
from cl.runtime.tasks.celery.celery_queue import celery_start_queue

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

    # TODO (Roman): save all logs to db
    # Save log entry to the database
    log_type = UserLogEntry if isinstance(exc, UserError) else LogEntry
    entry = log_type(  # noqa
        message=str(exc),
        level=log_level,
    )
    entry.init()
    Context.current().save_one(entry)

    # Message to display for user
    user_message = str(exc) if log_level == LogEntryLevelEnum.USER_ERROR else None

    # Return 500 response to avoid exception handler multiple calls
    # IMPORTANT:
    # - If UserMessage is set it will be shown to the user on toast badge and bell becomes red,
    # - Otherwise default message will be shown
    # TODO: Make it possible to customize default message in client code or pass from settings via runtime
    return JSONResponse({"UserMessage": user_message}, status_code=500)


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


# Get CORSMiddleware settings defined in Dynaconf from ApiSettings
api_settings = ApiSettings.instance()
server_app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.allow_origins,
    allow_origin_regex=api_settings.allow_origin_regex,
    allow_credentials=api_settings.allow_credentials,
    allow_methods=api_settings.allow_methods,
    allow_headers=api_settings.allow_headers,
    expose_headers=api_settings.expose_headers,
    max_age=api_settings.max_age,
)

# Middleware for executing each API call in isolated context
server_app.add_middleware(ContextMiddleware)

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
        log_dir = os.path.join(ProjectSettings.get_project_root(), "logs")  # TODO: Make unique
        celery_start_queue(log_dir=log_dir)

        # Save records from preload directory to DB and execute run_configure on all preloaded Config records
        PreloadSettings.instance().save_and_configure()

        # Find wwwroot directory, error if not found
        wwwroot_dir = ProjectSettings.get_wwwroot()

        # Mount static client files
        server_app.mount("/", StaticFiles(directory=wwwroot_dir, html=True))

        # Open new browser tab in the default browser using http protocol.
        # It will switch to https if cert is present.
        webbrowser.open_new_tab(f"http://{api_settings.hostname}:{api_settings.port}")

        # Run Uvicorn using hostname and port specified by Dynaconf
        api_settings = ApiSettings.instance()
        uvicorn.run(server_app, host=api_settings.hostname, port=api_settings.port)
