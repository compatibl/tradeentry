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

from typing import Iterable, List


class ClRecordUtil:
    """Helper methods for ClRecord."""

    def composite_pk(*tokens) -> str:
        """
        Convert tokens to primary key string, surrounding any strings that
        contain semicolon with curly brackets.

        Examples:

        * (rt.Type1, A, B) -> 'rt.Type1;A;B'
        * (rt.Type2, rt.Type1;A;B, C) -> 'rt.Type2;{rt.Type1;A;B};C'
        * (rt.Type3, rt.Type2;{rt.Type1;A;B};C, D) -> 'rt.Type3;{rt.Type2;{rt.Type1;A;B};C};D'
        """
        escaped_tokens = [f'{{{t}}}' if ';' in str(t) else str(t) for t in tokens]
        return ';'.join(escaped_tokens)

    @staticmethod
    def split_simple_pk(pk: str) -> List[str]:
        """
        Split simple primary key string into tokens. Check that the key
        does not contain embedded keys surrounded by curly brackets.

        Example:

        * 'rt.Type1;A;B' -> [rt.Type1, A, B]
        * 'rt.Type2;{rt.Type1;A;B};C' -> Error, contains an embedded key
        """

        # Split by semicolon first
        tokens = pk.split(';')

        if not any([t.startswith('{') for t in tokens]):
            # If none of the tokens start from an opening curly brace, we are done.
            return tokens
        else:
            raise RuntimeError(f'Key {pk} is composite (contains embedded keys).')

    @staticmethod
    def split_composite_pk(pk: str) -> List[str]:
        """
        Split composite primary key string into tokens, removing curly brackets around
        tokens that are embedded keys but without performing recursive splitting
        of such embedded keys.

        Examples:

        * 'rt.Type1;A;B' -> [rt.Type1, A, B]
        * 'rt.Type2;{rt.Type1;A;B};C' -> [rt.Type2, rt.Type1;A;B, C]
        * 'rt.Type3;{rt.Type2;{rt.Type1;A;B};C};D' -> [rt.Type3, rt.Type2;{rt.Type1;A;B};C, D]
        """

        # Split by semicolon first
        tokens = pk.split(';')

        opening_brace = [t.startswith('{') for t in tokens]
        if not any(opening_brace):
            # If none of the tokens start from an opening curly brace, we are done.
            return tokens
        else:
            # If at least one token starts from a curly bracket, we need to escape
            # semicolons inside the curly brackets taking into account that there
            # can be several.
            closing_brace = [t.endswith('}') for t in tokens]
            zipped = zip(tokens, opening_brace, closing_brace)
            result = []
            composite = []
            brace_level = 0
            for token, has_opening, has_closing in zipped:
                if has_opening:
                    if brace_level == 0:
                        # Remove brace from token only if initially at zero level
                        token = token[1:]
                    # Always increase level
                    brace_level = brace_level + 1
                    composite.append(token)
                elif has_closing:
                    # Always decrease level
                    brace_level = brace_level - 1
                    if brace_level == 0:
                        # Remove brace from token and finalize composite key if at zero level
                        token = token[:-1]
                        composite.append(token)
                        result.append(';'.join(composite))
                        composite = []
                    else:
                        composite.append(token)
                elif brace_level > 0:
                    composite.append(token)
                elif brace_level == 0:
                    result.append(token)
                else:
                    raise RuntimeError(f'More closing than opening curly braces in primary key {pk}')

            # Check for unbalanced braces
            if brace_level < 0:
                raise RuntimeError(f'More closing than opening curly braces in primary key {pk}')
            if brace_level > 0 or len(composite) > 0:
                raise RuntimeError(f'More opening than closing curly braces in primary key {pk}')

            return result
