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

from cl.convince.retrievers.retriever_key import RetrieverKey

cls = RetrieverKey


class RetrieverKeys:
    """RetrieverKey constants."""

    ANNOTATING_RETRIEVER: cls = cls(retriever_id="AnnotatingRetriever")
    """Instructs the model to surround the requested parameter by curly braces and uses the annotations to retrieve."""
