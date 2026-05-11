import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

class Somewho:
    def __init__(self, key: bytes):
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
        ).derive(key)
        self.chacha = ChaCha20Poly1305(derived_key)

    def encrypt(self, message: str):
        nonce = os.urandom(12)
        aad = b"header info"
        ciphertext = self.chacha.encrypt(nonce, message.encode(), aad)
        return nonce, ciphertext

    def decrypt(self, nonce: bytes, ciphertext: bytes):
        aad = b"header info"
        return self.chacha.decrypt(nonce, ciphertext, aad).decode()

key = b"key"
a = Somewho(key)
b = Somewho(key)

nonce, ciphertext = a.encrypt("Some text")
print(ciphertext.hex())
print(b.decrypt(nonce, ciphertext))