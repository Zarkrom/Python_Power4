#!/usr/bin/env python
import asyncio
import websockets
import json
from power4 import PLAYER1, PLAYER2

""" Fichier principal du serveur
    Contient une boucle infinie d'écoute : main() sur localhost:8001
    et une fonction appelée à chaque message entrant : handler 
        ... qui fait un print du message
"""

async def handler(websocket):
    redTurn = True
    while True:
        # Lecture du message envoyé par le navigateur
        async for message in websocket:
            # A chaque tour on change de joueur
            player = PLAYER1 if redTurn else PLAYER2
            redTurn = not redTurn
            event = json.loads(message)
            assert event["type"] == "play"
            column = event["column"]
            # On forge un objet JSON event
            event = {
                "type": "play",
                "player": player,
                "column": column,
                "row": 0, # Pour l'instant on ne sait jouer que sur la ligne du bas
            }
            # On l'envoi au navigateur pour affichage
            await websocket.send(json.dumps(event))


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())