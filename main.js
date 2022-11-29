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
  sendMoves(board, websocket);
  createBoard(board);
});

