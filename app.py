#!/usr/bin/env python
import asyncio
import websockets

""" Fichier principal du serveur
    Contient une boucle infinie d'écoute : main() sur localhost:8001
    et une fonction appelée à chaque message entrant : handler 
        ... qui fait un print du message
"""

async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        print(message)

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())