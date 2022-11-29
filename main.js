import { createBoard, playMove } from "./power4.js";

function sendMoves(board, websocket) {
  // Fonction qui envoie le clic au serveur
  board.addEventListener("click", ({ target }) => {
    // Je récupére la colonne cliquée
    const column = target.dataset.column;
    if (column === undefined) {
      // J'ignore les clics hors des colonnes
      return;
    }
    const event = {
      type: "play",
      // je convertit le N° de colonne en un interger en base 10
      column: parseInt(column, 10),
    };
    // J'envoie le message "play" au serveur aprés l'avoir linéarisé
    websocket.send(JSON.stringify(event));
  });
}

window.addEventListener("DOMContentLoaded", () => {
  // Dés que le DOM est chargé, on y ajoute le tableau de jeu
  const board = document.querySelector(".board");
  // Ouvrir la connexion WebSocket & enregistrer l'EventListener.
  const websocket = new WebSocket("ws://localhost:8001/");
  receiveMoves(board, websocket);
  sendMoves(board, websocket);
  createBoard(board);
});

function showMessage(message) {
  window.setTimeout(() => window.alert(message), 50);
}

function receiveMoves(board, websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "play":
        // Afficher le coup joué avec playMove de connect4.js.
        playMove(board, event.player, event.column, event.row);
        break;
      case "win":
        showMessage(`Joueur ${event.player} à gagné !`);
        // Game over ! On ferme la connexion.
        websocket.close(1000);
        break;
      case "error":
        // Afficher le message envoyé par le serveur
        showMessage(event.message);
        break;
      default:
        throw new Error(`Unsupported event type: ${event.type}.`);
    }
  });
}

