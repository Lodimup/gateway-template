from appaccount.models.accounts import User
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/demo/chat/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
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


@router.get("/")
async def get():
    return HTMLResponse(html)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json({"message": message})

    async def broadcast(self, message: str):
        """
        Broadcast to all clients connected to `this` FastAPI instances.
        To broadcast to all clients connected to all FastAPI instances, use RabbitMQ.
        """
        for connection in self.active_connections:
            await connection.send_json({"message": message})


manager = ConnectionManager()


@router.websocket("/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    "Demonstrates how to use Django ORM in FastAPI websocket"
    await manager.connect(websocket)
    user = await User.objects.all().afirst()
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(
                f"You wrote: {data} {user.username}", websocket
            )
            await manager.broadcast(f"Client #{client_id} says: {data}")
            async for user in User.objects.all()[:5]:
                await manager.broadcast(f"Client #{client_id} says: {user.username}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
