#!/usr/bin/env python

import asyncio
import json
import websockets
import uuid


async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your user name? ")
        device_mac = (hex(uuid.getnode()))
        connect_message = {
            "type": "connect",
            "user": name,
            "device": device_mac
        }
        await websocket.send(json.dumps(connect_message))
        token = websocket.recv()
        print(f"Connected to the server with token: {token}")
        # START THE LISTENER AND SENDER
        receive_task = asyncio.create_task(receive_messages(websocket))
        send_task = asyncio.create_task(send_messages(websocket, name))
        await asyncio.gather(receive_task, send_task)


async def send_messages(websocket, name):
    # SERVICE LOOP
    while True:
        body = input("Enter message: ")
        to = "edwinariza"
        message = {
            'type': 'message',
            'body': body,
            'from': name,
            'to': to
        }
        await websocket.send(json.dumps(message))
        print(f"Sent: {message}")


async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(f"Mensaje recibido del servidor: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        print("La conexión con el servidor se ha cerrado.")


if __name__ == "__main__":
    asyncio.run(main())






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



