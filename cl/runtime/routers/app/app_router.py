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
from fastapi import APIRouter
from starlette import status
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from cl.runtime.settings.settings import Settings

router = APIRouter()


@router.get(
    path="/",
    description="Redirect to a specific endpoint for the frontend app to load index.html.",
    response_class=RedirectResponse,
)
async def get_app_index_root():
    """
    Redirect to '/app' endpoint for the frontend app to load index.html.

    Returns:
    RedirectResponse: Redirects to '/app' with status code 301 (Moved Permanently).
    """
    return RedirectResponse("/app", status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.get(
    path="/app{_:path}",
    description="Get application index.html file ignoring paths after the endpoint paths.",
    response_class=HTMLResponse,
)
async def get_app_index(_):
    """
    Retrieve the application's index.html file while ignoring paths after the endpoint paths.

    Parameters:
    - _: Placeholder parameter to capture the path.

    Returns:
    HTMLResponse: The content of the index.html file.

    Raises:
    RuntimeError: If the index.html file or static files directory is not found.
    """

    static_dir = Settings.get_wwwroot_dir()
    if static_dir:
        index_file = os.path.join(static_dir, "index.html")
        if os.path.isfile(index_file):
            with open(index_file, "r") as file:
                return file.read()
    return RedirectResponse(url="/docs")
