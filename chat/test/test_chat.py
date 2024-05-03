# import websocket

# ws = websocket.WebSocket()
# ws.connect("ws://localhost:5000/chat/foo/ws?token=some-key-token")
# ws.send("Hello, Server")
# print(ws.recv())
# ws.close()


# def on_message(wsapp, message):
#     print(message)


# wsapp = websocket.WebSocketApp(
#     "ws://localhost:5000/chat/foo/ws?token=some-key-token", on_message=on_message
# )
# wsapp.run_forever()


import asyncio
import websockets

import pytest
from httpx import AsyncClient
import json

from ..app import app

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
@pytest.mark.parametrize(
    "data,expected_status_code, expected_resp",
    [
        (
            {
                "username": "alice",
                "email": "alice.chen@example.com",
                "password": "password123",
                "grant_type": "password",
            },
            200,
            {
                "token_type": "bearer",
            },
        ),
    ],
)
async def test_websocket_endpoint(data, expected_status_code, expected_resp):

    async with AsyncClient() as ac:
        response = await ac.post(
            "http://vahshipanda-api:5000/users/token",
            data=data,
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
    access_token = response.json()["access_token"]

    data = {
        "action": "send_message",
        "chat_channel_id": "660998602dc04e6f4d060562",
        "msg_from:": "James",
        "msg_to": "Mehdi",
        "content": "msg from unit test",
    }
    data_str = json.dumps(data)

    uri = f"ws://localhost:5000/chat/ws?token={access_token}"
    async with websockets.connect(uri) as ws:
        await ws.send(data_str)
        greeting = await ws.recv()
        print(f"Received: {greeting}")


# Run the coroutine
# asyncio.run(websocket_client())
