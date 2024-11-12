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
from typing import List
from cl.runtime.settings.settings import Settings


@dataclass(slots=True, kw_only=True)
class ApiSettings(Settings):
    """
    REST API and CORS (cross-origin resource sharing) settings.

    Notes:
        - Defaults are applied only if host name is None, localhost, or 127.0.0.1
        - For other hostnames, essential CORS parameters become required
    """

    hostname: str | None = None
    """REST API hostname or IP address."""

    port: int | None = None
    """REST API port."""

    allow_origins: List[str] | None = None
    """The list of origins allowed to make cross-origin requests, must include hostname for the UI to run."""

    allow_origin_regex: str | None = None
    """A regex string to match against origins to allow cross-origin requests."""

    allow_credentials: bool | None = None
    """Allows cookies and other credentials to be sent in cross-origin requests."""

    allow_methods: List[str] | None = None
    """The list of HTTP methods allowed for cross-origin requests (e.g., "GET", "POST")."""

    allow_headers: List[str] | None = None
    """The list of HTTP request headers allowed for cross-origin requests."""

    expose_headers: List[str] | None = None
    """The list of headers that browsers are allowed to access."""

    max_age: int | None = None
    """Maximum time in seconds for browsers to cache the CORS response."""

    def init(self) -> None:
        """Same as __init__ but can be used when field values are set both during and after construction."""

        # Validate hostname
        if self.hostname is not None and not isinstance(self.hostname, str):
            raise RuntimeError(f"{type(self).__name__} field 'hostname' must be a string or None.")

        # Convert and validate port
        if self.port is None or isinstance(self.port, int):
            pass
        elif isinstance(self.port, str):
            if self.port.isdigit():
                self.port = int(self.port)
            else:
                raise RuntimeError(f"{type(self).__name__} field 'port' includes non-digit characters.")
        else:
            raise RuntimeError(f"{type(self).__name__} field 'port' must be an int or a string.")

        # Apply the defaults to the remaining fields when hostname is one of None, localhost or loopback IP address
        if self.hostname in [None, "localhost", "127.0.0.1"]:
            if self.hostname is None:
                self.hostname = "localhost"
            if self.port is None:
                self.port = 7008
            if self.allow_origins is None:
                # Allow both localhost and loopback IP because the users consider them interchangeable
                self.allow_origins = ["localhost", "127.0.0.1"]
            if self.allow_credentials is None:
                self.allow_credentials = True
            if self.allow_methods is None:
                self.allow_methods = ["*"]
            if self.allow_headers is None:
                self.allow_headers = ["*"]

        # Validate the remaining settings,
        if self.allow_origins is None:
            raise RuntimeError(f"{type(self).__name__} field 'allow_origins' is required except for localhost.")
        elif isinstance(self.allow_origins, str) or not hasattr(self.allow_origins, "__iter__"):
            raise RuntimeError(f"{type(self).__name__} field 'allow_origins' must be a list or None.")

        if self.allow_origin_regex is not None and not isinstance(self.allow_origin_regex, str):
            raise RuntimeError(f"{type(self).__name__} field 'allow_origin_regex' must be a string or None.")

        if self.allow_credentials is None:
            raise RuntimeError(f"{type(self).__name__} field 'allow_credentials' is required except for localhost.")
        elif not isinstance(self.allow_credentials, bool):
            raise RuntimeError(f"{type(self).__name__} field 'allow_credentials' must be a bool or None.")

        if self.allow_methods is None:
            raise RuntimeError(f"{type(self).__name__} field 'allow_methods' is required except for localhost.")
        elif isinstance(self.allow_methods, str) or not hasattr(self.allow_methods, "__iter__"):
            raise RuntimeError(f"{type(self).__name__} field 'allow_methods' must be a list or None.")

        if self.allow_headers is None:
            raise RuntimeError(f"{type(self).__name__} field 'allow_headers' is required except for localhost.")
        elif isinstance(self.allow_headers, str) or not hasattr(self.allow_headers, "__iter__"):
            raise RuntimeError(f"{type(self).__name__} field 'allow_headers' must be a list or None.")

        if self.expose_headers is not None and (
            isinstance(self.expose_headers, str) or not hasattr(self.expose_headers, "__iter__")
        ):
            raise RuntimeError(f"{type(self).__name__} field 'expose_headers' must be a list or None.")

        if self.max_age is not None and not isinstance(self.max_age, int):
            raise RuntimeError(f"{type(self).__name__} field 'max_age' must be an int or None.")

    @classmethod
    def get_prefix(cls) -> str:
        return "runtime_api"
