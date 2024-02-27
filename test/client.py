import asyncio
import websockets


async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(f"Mensaje recibido del servidor: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        print("La conexión con el servidor se ha cerrado.")


async def send_messages(websocket):
    try:
        while True:
            message = input("Ingrese su mensaje: ")
            await websocket.send(message)
            print("Mensaje enviado al servidor")
    except websockets.exceptions.ConnectionClosedOK:
        print("La conexión con el servidor se ha cerrado.")


async def main():
    uri = "ws://localhost:8765"  # Reemplaza con la URL del servidor WebSocket

    async with websockets.connect(uri) as websocket:
        receive_task = asyncio.create_task(receive_messages(websocket))
        send_task = asyncio.create_task(send_messages(websocket))

        await asyncio.gather(receive_task, send_task)

asyncio.run(main())