# cryptography
my message encryption implementation

## X25519
X25519 даёт нам два одинаковых ключа на рзных сторонах. Он сам ассиметричный, а даёт кайфовые симметричные ключи
```python
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
```

## HKDF
Этот бро нам просто даёт ключ нужной длинны на базе существующего ключа
```python
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
```

## ChaCha20Poly1305
Собственно само шифроввание
```python
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
```

# Usage
## 1. Сгенерировать ключи
```python
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
```

## 2.Сервер(websoket)
```python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import crypt_ws
from crypt import CryptoUtils
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

app = FastAPI()
private_bytes = Path("k_private").read_bytes()
k_sign_priv = serialization.load_pem_private_key(private_bytes, password=None)

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        peer = crypt_ws.Communicator_server(websocket, k_sign_priv)
        await peer.exchange()
        await peer.send("hello everyone!")
        print(await peer.receive())
        print(await peer.receive())
        print(await peer.receive())
    except WebSocketDisconnect:
        print("Client disconnected")
```
Run:
```bash
uvicorn samples.server:app --port 2002
```

# 3. Клиент
```python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio, websockets, crypt_ws
from pathlib import Path

async def hello():
    k_sign_pub = Path("k_public").read_text(encoding="utf-8")
    async with websockets.connect("ws://localhost:2002/") as websocket:
        peer = crypt_ws.Communicator_client(websocket, k_sign_pub)
        await peer.exchange()
        print(await peer.receive())
        await peer.send("hi from your slave")
        await peer.send("lorem inspum")
        await peer.send("dolor sit amet")

asyncio.run(hello())
```