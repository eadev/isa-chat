import asyncio
import websockets

connected_clients = set()


async def handle_client(websocket, path):
    # Agregar cliente a la lista de clientes conectados
    connected_clients.add(websocket)
    print(f"Nueva conexión establecida: {websocket}")

    try:
        async for message in websocket:
            print(f"Mensaje recibido de cliente: {message}")
            # Reenviar mensaje a todos los clientes conectados
            for client in connected_clients:
                if client != websocket:
                    print("SENDING MESSAGE TO CLIENTS")
                    print(client)
                    await client.send(message)
    except websockets.exceptions.ConnectionClosedOK:
        pass
    finally:
        # Remover cliente de la lista de clientes conectados
        connected_clients.remove(websocket)
        print(f"Conexión cerrada: {websocket}")


async def main():
    # Configurar el servidor WebSocket
    async with websockets.serve(handle_client, "localhost", 8765):
        print("Servidor WebSocket iniciado en ws://localhost:8765")
        await asyncio.Future()  # Mantener el servidor en funcionamiento

asyncio.run(main())