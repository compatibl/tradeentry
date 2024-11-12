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

import pytest
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cl.runtime.context.context_util import ContextUtil
from cl.runtime.context.testing_context import TestingContext


def _generate_rsa_private_cert() -> str:
    # Generate private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

    # Convert private key to PEM format
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    # Convert PEM bytes to string
    pem_str = pem.decode("utf-8")
    return pem_str


def _encrypt_value(value: str) -> str:
    public_key_pem = None
    raise NotImplementedError()

    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    encrypted = public_key.encrypt(
        value.encode(),
        padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    return base64.b64encode(encrypted).decode()


@pytest.mark.skip("Requires RSA key to decrypt.")
def test_decrypt_secret():
    """Test ContextUtil.decrypt_secret method."""

    with TestingContext() as context:

        key = "test_key"
        value = "secret_value"
        encrypted_value = _encrypt_value(value)
        context.secrets[key] = encrypted_value
        secret_value_decrypted = ContextUtil.decrypt_secret(key)
        assert secret_value_decrypted == value


if __name__ == "__main__":
    pytest.main([__file__])
