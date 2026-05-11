from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

class Somewho:
    def __init__(self):
        self.priv = x25519.X25519PrivateKey.generate()

    def say(self):
        return self.priv.public_key()

    def listen(self, key: x25519.X25519PublicKey):
        return self.priv.exchange(key)

a = Somewho()
b = Somewho()

pub1 = a.say()
print("a -> b:", pub1.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw).hex())
print("b:", b.listen(pub1).hex())

pub2 = b.say()
print("b -> a:", pub2.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw).hex())
print("a:", a.listen(pub2).hex())