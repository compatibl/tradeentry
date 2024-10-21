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
from cl.runtime.primitive.case_util import CaseUtil


class EnvUtil:
    """Helper methods for environment selection."""

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
        test_module_pattern = "test_"

        stack = inspect.stack()
        for frame_info in stack:
            filename = os.path.basename(frame_info.filename)
            if filename.startswith(test_module_pattern) and filename.endswith(".py"):
                return True
        return False

    @classmethod
    def get_env_dir(
        cls,
        *,
        default_dir: str | None = None,
        test_function_pattern: str | None = None,
    ) -> str:
        """
        Return module_dir/test_module/test_function or module_dir/test_module/test_class/test_method,
        collapsing levels with identical name into one.

        Notes:
            Implemented by searching the stack frame for 'test_' or a custom test function name pattern.

        Args:
            default_dir: When not running inside a test, return this directory if specified, error if not specified
            test_function_pattern: Glob pattern for function or method in stack frame, defaults to 'test_*'
        """
        result = cls._get_test_env_dir_or_name(
            is_name=False,
            test_function_pattern=test_function_pattern,
        )

        # If the end of the frame is reached and no function or method starting from test_ is found,
        # the function was not called from inside a test and default_dir will be returned if specified
        if result is None:
            if default_dir is not None and default_dir != "":
                result = default_dir
            else:
                RuntimeError(
                    f"Not invoked inside a function or method that starts from '{test_function_pattern}' "
                    f"and 'default_dir' is None or empty."
                )
        return result

    @classmethod
    def get_env_name(
        cls,
        *,
        test_function_pattern: str | None = None,
    ) -> str:
        """
        Return module_dir/test_module.test_function or module_dir/test_module.test_class.test_method,
        collapsing levels with identical name into one.

        Notes:
            Implemented by searching the stack frame for 'test_' or a custom test function name pattern.

        Args:
            test_function_pattern: Glob pattern for function or method in stack frame, defaults to 'test_*'
        """

        # Get test environment if inside test
        result = cls._get_test_env_dir_or_name(
            is_name=True,
            test_function_pattern=test_function_pattern,
        )

        # Otherwise assign default name
        if result is None:
            result = "main"
        return result

    @classmethod
    def _get_test_env_dir_or_name(
        cls,
        *,
        is_name: bool,
        test_function_pattern: str | None = None,
    ) -> str | None:
        """
        Return test_module.test_function or test_module.test_class.test_function by searching the stack frame
        for 'test_' or a custom test function name pattern.

        Args:
            is_name: If True, return dot delimited name, otherwise return directory path
            test_function_pattern: Glob pattern for function or method in stack frame, defaults to 'test_*'
        """

        if test_function_pattern is not None:
            # TODO: Support custom patterns
            raise RuntimeError("Custom test function or method name patterns are not yet supported.")
        test_function_pattern = "test_"

        stack = inspect.stack()
        for frame_info in stack:
            if frame_info.function.startswith(test_function_pattern):
                frame_globals = frame_info.frame.f_globals
                module_file = frame_globals["__file__"]
                test_name = frame_info.function
                cls_instance = frame_info.frame.f_locals.get("self", None)
                class_name = cast(type, cls_instance).__class__.__name__ if cls_instance else None

                if module_file.endswith(".py"):
                    module_file_without_ext = module_file.removesuffix(".py")
                else:
                    raise RuntimeError(f"Test module file {module_file} does not end with '.py'.")

                # Determine delimiter based on is_name flag
                delim = "." if is_name else os.sep

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
                    class_name = CaseUtil.pascal_to_snake_case(class_name)

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
                if not is_name:
                    result = os.path.join(module_dir, result)
                return result

        # Not inside test, return None
        return None
