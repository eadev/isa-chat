#!/usr/bin/env python

import asyncio
import json
import uuid

from websockets.server import serve

USERS = []


async def handler(websocket):
    async for message in websocket:
        # TRANSFORM THE MESSAGE TO JSON
        message_receive = json.loads(message)
        print(message_receive)
        # ADD NEW USER TO THE SET
        if message_receive["type"] == "connect":
            # GENERATE A TOKEN FOR THE USER
            token = uuid.uuid4()
            USERS.append({"websocket": websocket, "name": message_receive["user"], "token": token})
            print(f"New user connected: {message_receive['user']}")
            await websocket.send(str(token))
        elif message_receive["type"] == "message":
            # ECHO MESSAGE TO ALL USERS
            for USER in USERS:
                if USER["websocket"] != websocket:
                    member = USER['websocket']
                    print(message_receive)
                    # SEND MESSAGE TO THE USER
                    await member.send(json.dumps(message_receive))
        else:
            print(f"Unknown message type: {message_receive['type']}")


async def main():
    print("Isa-Chat Server running on ws://localhost:8765 (Press CTRL+C to quit)")
    print("Developed by Edwin Ariza")
    async with serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())