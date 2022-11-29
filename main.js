import { createBoard, playMove } from "./power4.js";

window.addEventListener("DOMContentLoaded", () => {
  // Dés que le DOM est chargé, on y ajoute le tableau de jeu
  const board = document.querySelector(".board");
  createBoard(board);
});
