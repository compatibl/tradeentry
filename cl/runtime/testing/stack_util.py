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
import os
from typing import cast
import inflection


class StackUtil:
    """Utilities for stack introspection."""

    @classmethod
    def is_inside_test(cls, *, test_module_pattern: str | None = None) -> bool:
        """
        Return True if invoked from a test, detection is based on test module pattern.

        Args:
            test_module_pattern: Glob pattern to identify the test module, defaults to 'test_*.py'
        """

        if test_module_pattern is not None:
            # TODO: test_module_pattern custom patterns
            raise RuntimeError("Custom test module patterns are not yet supported.")

        stack = inspect.stack()
        for frame_info in stack:
            filename = os.path.basename(frame_info.filename)
            if filename.startswith("test_") and filename.endswith(".py"):
                return True
        return False

    @classmethod
    def get_base_dir(
        cls,
        *,
        allow_missing: bool = False,
        test_function_pattern: str | None = None,
    ) -> str:
        """
        Return module_dir/test_module/test_function or module_dir/test_module/test_class/test_method,
        collapsing levels with identical name into one.

        Notes:
            Implemented by searching the stack frame for 'test_' or a custom test function name pattern.

        Args:
            allow_missing: If True, return None if path is not found (e.g. when not running inside a test)
            test_function_pattern: Glob pattern to identify the test function or method in stack frame,
            defaults to 'test_*'
        """
        return cls._get_base_dir_or_path(
            dot_delimited=False, allow_missing=allow_missing, test_function_pattern=test_function_pattern
        )

    @classmethod
    def get_base_path(
        cls,
        *,
        allow_missing: bool = False,
        test_function_pattern: str | None = None,
    ) -> str:
        """
        Return module_dir/test_module.test_function or module_dir/test_module.test_class.test_method,
        collapsing levels with identical name into one.

        Notes:
            Implemented by searching the stack frame for 'test_' or a custom test function name pattern.

        Args:
            allow_missing: If True, return None if path is not found (e.g. when not running inside a test)
            test_function_pattern: Glob pattern to identify the test function or method in stack frame,
            defaults to 'test_*'
        """
        return cls._get_base_dir_or_path(
            dot_delimited=True, allow_missing=allow_missing, test_function_pattern=test_function_pattern
        )

    @classmethod
    def _get_base_dir_or_path(  # TODO: Refactor to return tuple of dir and name and rename method after refactoring
        cls,
        *,
        dot_delimited: bool,
        allow_missing: bool = False,
        test_function_pattern: str | None = None,
    ) -> str:
        """
        Return test_module.test_function or test_module.test_class.test_function by searching the stack frame
        for 'test_' or a custom test function name pattern.

        Args:
            dot_delimited: If True, test module, class and method are dot-delimited rather than directory levels
            allow_missing: If True, return None if path is not found (e.g. when not running inside a test)
            test_function_pattern: Glob pattern to identify the test function or method in stack frame,
            defaults to 'test_*'
        """

        if test_function_pattern is not None:
            # TODO: Support custom patterns
            raise RuntimeError("Custom test function or method name patterns are not yet supported.")

        stack = inspect.stack()
        for frame_info in stack:
            if frame_info.function.startswith("test_"):
                frame_globals = frame_info.frame.f_globals
                module_file = frame_globals["__file__"]
                test_name = frame_info.function
                cls_instance = frame_info.frame.f_locals.get("self", None)
                class_name = cast(type, cls_instance).__class__.__name__ if cls_instance else None

                if module_file.endswith(".py"):
                    module_file_without_ext = module_file.removesuffix(".py")
                else:
                    raise RuntimeError(f"Test module file {module_file} does not end with '.py'.")

                # Determine delimiter based on dot_delimited flag
                delim = "." if dot_delimited else os.sep

                module_dir = os.path.dirname(module_file_without_ext)
                module_name = os.path.basename(module_file_without_ext)
                if class_name is None:
                    # Remove repeated identical tokens to shorten the path
                    if module_name != test_name:
                        result = delim.join((module_name, test_name))
                    else:
                        result = module_name
                else:
                    # Convert class name to snake_case
                    class_name = inflection.underscore(class_name)

                    # Remove repeated identical tokens to shorten the path
                    if module_name != class_name:
                        if class_name != test_name:
                            result = delim.join((module_name, class_name, test_name))
                        else:
                            result = delim.join((module_name, class_name))
                    else:
                        if module_name != test_name:
                            result = delim.join((module_name, test_name))
                        else:
                            result = module_name
                result = os.path.join(module_dir, result)
                return result

        if allow_missing:
            # Return None if path is not found (e.g. when not running inside a test)
            return None
        else:
            # If the end of the frame is reached and no function or method starting from test_ is found,
            # the function was not called from inside a test or a custom match pattern is required
            raise RuntimeError("Not invoked inside a function or method that starts from 'test_'.")
