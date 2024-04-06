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

import inspect
from cl.runtime.attributes.handler_decorator import handler
from cl.runtime.attributes.implement_language import ImplementLanguage
from cl.runtime.attributes.method_trait import MethodTrait


def viewer(
    *args: MethodTrait,
    language: ImplementLanguage = ImplementLanguage.Python,
    view_name: str = None,
    view_type: str = None,
):
    """
    Decorator for identifying viewer methods.

    Viewers are methods that create View records that
    are displayed along with the record in the user interface,
    e.g. on a tab of the screen associated with the Record.

    Note that not all View records are created by viewer
    methods. Some may be created as side effect of a handler,
    by the record's Init method, or even by an unrelated data
    type.

    A viewer method must not take any parameters and have
    no return value.

    View record created by the viewer must have ViewName
    that matches the value specified in the attribute constructor,
    or if not specified, the name of the viewer method.
    """

    def wrap(method):
        if not inspect.isfunction(method) and not inspect.ismethod(method):
            raise Exception('@viewer decorator should be applied on method or function.')

        method = handler(*args, language=language)(method)
        method._cl_viewer = True
        method._cl_viewer_view_name = view_name
        method._view_type = view_type
        return method

    if len(args) == 1:
        maybe_method = args[0]
        if inspect.isfunction(maybe_method) or inspect.ismethod(maybe_method):
            maybe_method = handler(language=language)(maybe_method)
            maybe_method._cl_viewer = True
            maybe_method._cl_viewer_view_name = view_name
            maybe_method._view_type = view_type
            return maybe_method

    return wrap
