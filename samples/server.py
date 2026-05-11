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