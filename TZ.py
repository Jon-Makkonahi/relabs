from typing import Union

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Чат (Тестовое задание)</title>
    </head>
    <body>
        <h1>WebSocket Чат</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Отправитель: <input type="text" id="itemId" autocomplete="off"/></label>
            <label>Токен: <input type="text" id="token" autocomplete="off"/></label>
            <button onclick="connect(event)">Подключиться</button>
            <hr>
            <label>Сообщение: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Отправить</button>
        </form>
        <ol id='messages'>
        </ol>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
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


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    item_id: str,
    q: Union[int, None] = None,
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if q is not None:
            await websocket.send_text(f"{q}")
        await websocket.send_text(f"Сообщение:{data} - отправил: {item_id}")
