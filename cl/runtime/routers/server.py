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

from cl.runtime.routers.auth import auth_router
from cl.runtime.routers.entity import entity_router
from cl.runtime.routers.health import health_router
from cl.runtime.routers.schema import schema_router
from cl.runtime.routers.storage import storage_router
from cl.runtime.settings.runtime_settings import RuntimeSettings
from fastapi import FastAPI
from pathlib import Path
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

# Server
app = FastAPI()

# Get Runtime settings from Dynaconf
runtime_settings = RuntimeSettings.instance()

# Permit origins based on either hostname or host IP
origins = [
    f"{runtime_settings.api_host_name}:{runtime_settings.api_port}",
    f"{runtime_settings.api_host_ip}:{runtime_settings.api_port}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Specify allowed HTTP methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # Specify allowed headers, e.g., ["Content-Type", "Authorization"]
)


# Routers
app.include_router(health_router.router, prefix="", tags=["Health Check"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authorization"])
app.include_router(schema_router.router, prefix="/schema", tags=["Schema"])
app.include_router(storage_router.router, prefix="/storage", tags=["Storage"])
app.include_router(entity_router.router, prefix="/entity", tags=["Entity"])

# Search locations for wwwroot directory
working_dir = Path().resolve()
module_path = Path(__file__)
ui_dir = "wwwroot"
locations = [d.joinpath(ui_dir) for d in (working_dir, module_path.parents[2], module_path.parents[3])]

# Use the first location where dir_name subdirectory exists
ui_path = None
for location in locations:
    if location.exists():
        ui_path = location

# Launch UI if ui_path is found
if ui_path is not None:
    app.mount("/", StaticFiles(directory=ui_path, html=True))
    print(f"Starting UI configuration in {ui_path}")
else:
    locations_str = "\n".join("    " + str(location) for location in locations)
    print(f"UI configuration not found, starting REST API only.\n" f"Directories searched:\n{locations_str}")
