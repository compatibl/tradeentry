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

import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cl.runtime import Context


class ContextUtil:
    """Helper methods for Context."""

    @classmethod
    def get_secret(cls, key: str) -> str | None:
        """Get the secret value for the specified key from Context.current().secrets, return None if not found."""

        # Get secrets field of the current context, return None if not specified
        secrets = Context.current().secrets
        if secrets is None:
            return None

        # Get secret by key, return None if key is not present
        encrypted_value = secrets.get(key)
        if encrypted_value is None:
            return None

        # Decode base64 encoded encrypted value
        encrypted_value_bytes = base64.b64decode(encrypted_value)

        # PEM encoded private key
        return None  # TODO: Temporarily return None
        private_key_pem: str = None

        # Load the private key
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None,
            backend=default_backend()
        )

        # Decrypt the value
        decrypted_value_bytes = private_key.decrypt(
            encrypted_value_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_value_bytes.decode('utf-8')
