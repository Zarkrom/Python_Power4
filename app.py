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
    game = Power4() # On instancie la classe Power4
    redTurn = True # C'est le rouge qui commence
    # Lecture du message envoyé par le navigateur
    async for message in websocket:
        # A chaque tour on change de joueur
        player = PLAYER1 if redTurn else PLAYER2
        redTurn = not redTurn
        # On lit un evenement "play" depuis le navigateur
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]
        try:
            # On joue le coup reçu
            row = game.play(player, column)
        except RuntimeError as exc:
            # On a reçu un evenement "error" pour coup illégal
            event = {
                "type": "error",
                "message": str(exc),
            }
            await websocket.send(json.dumps(event))
            continue
        # On forge un evenement "play" pour afficher sur le navigateur
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        await websocket.send(json.dumps(event))
        # Si ce dernier coup est gagnant : On envoie un evenement "win"
        if game.winner is not None:
            event = {
                "type": "win",
                "player": game.winner,
            }
        await websocket.send(json.dumps(event))


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())