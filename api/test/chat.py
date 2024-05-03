import websocket

# ws = websocket.WebSocket()
# ws.connect("ws://localhost:5000/chat/foo/ws?token=some-key-token")
# ws.send("Hello, Server")
# print(ws.recv())
# ws.close()


def on_message(wsapp, message):
    print(message)


wsapp = websocket.WebSocketApp(
    "ws://localhost:5000/chat/foo/ws?token=some-key-token", on_message=on_message
)
wsapp.run_forever()
