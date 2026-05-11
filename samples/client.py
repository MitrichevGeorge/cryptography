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