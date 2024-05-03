from fastapi.responses import HTMLResponse
from typing import Annotated
from fastapi import (
    Cookie,
    APIRouter,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from motor.motor_asyncio import AsyncIOMotorDatabase
from mongodb_app.database import get_chat_db
from mongodb_app import schemas
from mongodb_app import crud

import json
import httpx  # for async HTTP requests
import asyncio

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="chatId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:9001/chat/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get():
    return HTMLResponse(html)


# async def get_cookie_or_token(
#     websocket: WebSocket,
#     session: Annotated[str | None, Cookie()] = None,
#     token: Annotated[str | None, Query()] = None,
# ):
#     if session is None and token is None:
#         raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
#     return session or token


# @router.websocket("/{chat_id}/ws")
# async def websocket_endpoint(
#     *,
#     websocket: WebSocket,
#     chat_id: str,
#     q: int | None = None,
#     cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
# ):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(
#             f"Session cookie or query token value is: {cookie_or_token}"
#         )
#         if q is not None:
#             await websocket.send_text(f"Query parameter q is: {q}")
#         await websocket.send_text(f"Message text was: {data}, for item ID: {chat_id}")


# async def validate_token(
#     websocket: WebSocket,
#     session: Annotated[str | None, Cookie()] = None,
#     token: Annotated[str | None, Query()] = None,
# ) -> bool:

#     if session is None and token is None:
#         raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

#     # This function should implement the actual token validation logic
#     # For demonstration, let's assume it sends a request to a validation server
#     # Replace the URL with your validation server's URL
#     try:
#         print("validate_token is invoked!!!")
#         async with httpx.AsyncClient() as client:
#             response = await client.get(
#                 f"http://vahshipanda-api:5000/users/token_validate?token={token}"
#             )
#             return response.status_code == 200 and response.json().get("valid", False)
#     except httpx.RequestError as e:
#         print(f"An error occurred while requesting token validation: {e}")
#         return False


# @router.websocket("/ws")
# async def websocket_endpoint(
#     *,
#     websocket: WebSocket,
#     validate_token: Annotated[bool, Depends(validate_token)],
# ):
#     # Validate the token before accepting the connection
#     print("---------- websocket_endpoint ----------")
#     print(f"{validate_token=}")
#     # if not await validate_token(token):
#     #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#     #     return

#     if validate_token:
#         await websocket.accept()
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message text was: {data}")


# async def validate_token(token: str) -> bool:
#     # Mock validation function. Replace with actual validation logic.
#     # For example, you might make an HTTP request to a validation server.

#     print(f"{token=}")
#     return True
#     # try:
#     #     async with httpx.AsyncClient() as client:
#     #         response = await client.get(
#     #             f"http://validation-server/validate?token={token}"
#     #         )
#     #         if response.status_code == 200:
#     #             data = response.json()
#     #             return data.get("valid", False)
#     #         else:
#     #             return False
#     # except httpx.RequestError:
#     #     return False


async def validate_token(
    websocket: WebSocket,
    token: Annotated[str | None, Query()] = None,
) -> bool:

    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    # This function should implement the actual token validation logic
    # For demonstration, let's assume it sends a request to a validation server
    # Replace the URL with your validation server's URL
    try:
        async with httpx.AsyncClient(base_url="http://vahshipanda-api:5000") as client:
            response = await client.get(
                "/users/token_validate",
                headers={"Authorization": f"Bearer {token}"},
            )
            return response.status_code == 200 and response.json().get("valid", False)
    except httpx.RequestError as e:
        print(f"An error occurred while requesting token validation: {e}")
        return False


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    valid_token: Annotated[bool, Depends(validate_token)],
):

    if not valid_token:
        return
    await websocket.accept()
    try:
        while True:
            data_str = await websocket.receive_text()

            data = json.loads(data_str)

            action = data["action"]
            print(f"{action=}")

            if action == "send_message":
                await insert_msg(data)

            elif action == "retrive_message":
                retrive_msg(data)

            elif action == "delete_message":
                delete_msg(data)

            # await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")


async def insert_msg(
    data: dict,
    db: AsyncIOMotorDatabase = Depends(get_chat_db),
):
    msg = {
        "chat_channel_id": "65f53b1bb1bb952dca49a62b",
        "msg_from": "James",
        "msg_to": "James",
        "content": "This is a test message from James",
    }

    chat_channel_id = msg["chat_channel_id"]
    # del msg["chat_channel_id"]

    print("-" * 10)
    print(f"{data=}")

    msg = schemas.MessageInsert(**data)

    collection = "col1"
    result = crud.update_one(
        db,
        collection,
        chat_channel_id,
        msg,
    )
    print(result)

    return result


def retrive_msg():
    pass


def delete_msg():
    pass
