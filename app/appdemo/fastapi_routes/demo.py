"""
Demonstrate how to use RabbitMQ with FastAPI WebSockets
http://localhost:8080/demo/broadcaster/
"""

import asyncio
import uuid

import aio_pika
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WS Rabbitmq Producer/Consumer/Broadcaster demo</title>
    </head>
    <body>
        <h1>WS Rabbitmq Producer/Consumer/Broadcaster demo</h1>
        <form id="exchangeIdForm" onsubmit="setExchangeId(event)">
            <label for="exchangeId">Enter your Client ID:</label>
            <input type="text" id="exchangeId" autocomplete="off" required />
            <button type="submit">Set Client ID</button>
        </form>
        <div id="chatContainer" style="display: none;">
            <h2>Your ID: <span id="ws-id"></span></h2>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off" />
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
        </div>
        <script>
            let ws;

            function setExchangeId(event) {
                event.preventDefault();
                const clientIdInput = document.getElementById("exchangeId");
                const exchangeId = clientIdInput.value.trim();

                if (!exchangeId) {
                    alert("Client ID is required!");
                    return;
                }

                document.querySelector("#ws-id").textContent = exchangeId;
                document.getElementById("exchangeIdForm").style.display = "none";
                document.getElementById("chatContainer").style.display = "block";

                ws = new WebSocket(`ws://localhost:8080/ws/demo/broadcaster/${exchangeId}/`);
                ws.onmessage = function(event) {
                    const messages = document.getElementById('messages');
                    const message = document.createElement('li');
                    const content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };
            }

            function sendMessage(event) {
                event.preventDefault();
                const input = document.getElementById("messageText");
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(input.value);
                    input.value = '';
                } else {
                    alert("WebSocket connection is not open.");
                }
            }
        </script>
    </body>
</html>
"""


@router.get("/broadcaster/")
async def get():
    return HTMLResponse(html)


@router.websocket("/broadcaster/{exchange_id}/")
async def websocket_endpoint(websocket: WebSocket, exchange_id: str):
    "Demonstrates how to use Django ORM in FastAPI websocket"
    await websocket.accept()
    connection = websocket.app.state.aio_pika_connection
    async with connection:
        channel = await connection.channel()  # Create a channel
        exchange = await channel.declare_exchange(
            exchange_id, aio_pika.ExchangeType.FANOUT, durable=False
        )
        # create a unique queue for each websocket connection and bind it to the exchange
        queue = await channel.declare_queue(str(uuid.uuid4()), exclusive=True)
        await queue.bind(exchange)

        async def _consume_messages():
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        print(f"Received message: {message.body.decode()}")
                        await websocket.send_text(message.body.decode())

        # Start consuming messages in the background, allowing send / receive concurrently
        consume_task = asyncio.create_task(_consume_messages())

        try:
            while True:
                # Receive message from WebSocket
                data = await websocket.receive_text()
                print(f"Received from WebSocket: {data}")

                # Publish message to RabbitMQ
                await exchange.publish(
                    aio_pika.Message(body=data.encode()),
                    routing_key="chat",
                )
        except WebSocketDisconnect:
            print(f"WebSocket disconnected for exchange_id: {exchange_id}")
        finally:
            consume_task.cancel()
