import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cryptography.hazmat.primitives import serialization
from crypt import CryptoUtils
from pathlib import Path

sign_priv, sign_pub = CryptoUtils.generate_ed25519_keys()

private_bytes = sign_priv.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

Path("k_private").write_bytes(private_bytes)
Path("k_public").write_text(CryptoUtils.serialize_public_key(sign_pub), encoding="utf-8")