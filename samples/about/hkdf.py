from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
)
key = b"short"
print(key.hex())
print(hkdf.derive(key).hex())