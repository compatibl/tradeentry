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

import asyncio
import contextvars
from starlette.requests import Request
from starlette.types import ASGIApp
from cl.runtime.context.context import context_stack_var
from cl.runtime.context.process_context import ProcessContext


class ContextMiddleware:
    """
    Middleware to create an isolated context environment for API calls.

    - Create an isolated contextvars.Context as a copy of the current contextvars context.
    - Create an isolated runtime context stack.
    - Execute with the request-specific runtime Context.
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        # Copy contextvars.Context
        ctx = contextvars.copy_context()

        def init_context_stack():
            """Create isolated runtime contex stack as copy of current context stack."""

            # Get the current context stack value
            current_context_stack = context_stack_var.get()

            # Create a copy if the current context stack is not None
            new_context_stack = None if current_context_stack is None else [x for x in current_context_stack]

            # Set the copy as the new stack for the current asynchronous environment
            context_stack_var.set(new_context_stack)

        # Replace current context stack with a copy to avoid sharing the same context stack across requests
        ctx.run(init_context_stack)

        def call_in_event_loop():
            """A non-coroutine that we will run with contextvars.Context.run"""

            async def app_with_context():
                # Create a starlette request
                request = Request(scope, receive)

                # Create context with user-defined secrets
                secrets = {k: v for k, v in request.headers.items()}
                with ProcessContext(secrets=secrets):
                    await self.app(scope, receive, send)

            loop = asyncio.get_running_loop()
            return loop.create_task(app_with_context())

        # Execute request in isolated contextvars.Context
        await ctx.run(call_in_event_loop)
