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

import uvicorn
from cl.runtime.routers.server import app
from cl.runtime.settings.runtime_settings import RuntimeSettings
from stubs.cl.runtime.config.stub_runtime_config import StubRuntimeConfig  # TODO: Remove after refactoring

if __name__ == "__main__":

    # TODO: Temporary workaround before full configuration workflow is supported
    config = StubRuntimeConfig()
    config.config_id = "Stub Runtime Config"
    config.configure()

    # Run Uvicorn using hostname and port specified by Dynaconf
    runtime_settings = RuntimeSettings.instance()
    uvicorn.run(app, host=runtime_settings.api_host_name, port=runtime_settings.api_port)
