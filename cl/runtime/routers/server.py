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
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Server
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:7008",
    "http://localhost:3002",
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
