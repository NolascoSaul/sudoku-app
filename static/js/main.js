let selectedCell = null;

document.addEventListener("DOMContentLoaded", () => {
  const cells = document.querySelectorAll("#sudoku-board button");
  cells.forEach((btn) => {
    btn.addEventListener("click", () => {
      // No seleccionar si es celda fija
      if (btn.dataset.fixed === "1") return;

      const row = Number(btn.dataset.row);
      const col = Number(btn.dataset.col);
      selectedCell = { row, col };

      updateCellStyles();
    });
  });
});

/**
 * Actualiza los estilos de las celdas del tablero de Sudoku.
 *
 * - Las celdas fijas se marcan con un fondo gris y un cursor por defecto.
 * - La celda seleccionada se marca con un fondo gris oscuro.
 * - Las demás celdas se marcan con un fondo gris claro en hover.
 */
function updateCellStyles() {
  const cells = document.querySelectorAll("#sudoku-board button");
  cells.forEach((btn) => {
    if (btn.dataset.fixed === "1") {
      btn.classList.add("bg-gray-200", "cursor-default");
      btn.classList.remove(
        "hover:bg-gray-300",
        "cursor-pointer",
        "bg-gray-400"
      );
      return;
    }

    // Celda seleccionada
    if (selectedCell && btn.id === `${selectedCell.row}-${selectedCell.col}`) {
      btn.classList.add("bg-gray-400");
      btn.classList.remove("hover:bg-gray-300");
    } else {
      // Celdas no seleccionadas: hover activo
      btn.classList.remove("bg-gray-400");
      btn.classList.add("hover:bg-gray-300", "cursor-pointer");
    }
  });
}

/**
 * Inserta un número en una celda del tablero de Sudoku.
 *
 * Realiza una petición POST a "/insert" con un objeto payload que contiene la fila y columna de la celda seleccionada
 * y el número que se desea insertar en dicha celda.
 *
 * Si la petición falla, muestra un mensaje de error en una ventana emergente.
 * Si la petición tiene éxito, actualiza el tablero visual con el nuevo tablero de Sudoku generado.
 * Si la petición devuelve un error, muestra un mensaje de error en una ventana emergente.
 *
 * @param {number} num El número que se desea insertar en la celda seleccionada.
 * @returns {Promise<void>} Una promesa que se resuelve cuando se completa la petición.
 */
async function insertNumber(num) {
  if (!selectedCell) return;

  const payload = {
    row: selectedCell.row,
    col: selectedCell.col,
    num: Number(num),
  };

  const res = await fetch("/insert", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    alert("Error insert: " + (await res.text()));
    return;
  }

  const data = await res.json();
  updateBoardVisual(data.board);

  if (data.win) {
    winner();
    return;
  }

  if (data.error) alert(data.error);
}

/**
 * Elimina la celda seleccionada.
 *
 * Realiza una petición POST a "/erase" con el objeto payload que contiene la fila y columna de la celda seleccionada.
 *
 * @returns {Promise<void>} Una promesa que se resuelve cuando se completa la petición.
 */
async function eraseCell() {
  if (!selectedCell) return;

  const payload = {
    row: selectedCell.row,
    col: selectedCell.col,
  };

  const res = await fetch("/erase", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    console.error("Error erase:", await res.text());
    return;
  }

  const data = await res.json();
  updateBoardVisual(data.board);

  if (data.erases !== undefined) {
    const er = document.getElementById("erases");
    if (er) er.innerText = `${data.erases}/3`;
  }
}

/**
 * Reinicia el juego de Sudoku.
 *
 * Realiza una petición POST a "/reset" y actualiza el tablero visual
 * con el nuevo tablero de Sudoku generado.
 *
 * @returns {Promise<void>} Una promesa que se resuelve cuando se completa la petición.
 */
async function resetGame() {
  const res = await fetch("/reset", { method: "POST" });
  if (!res.ok) {
    console.error("Error reset:", await res.text());
    return;
  }

  const data = await res.json();
  selectedCell = null;
  updateBoardVisual(data.board, data.fixed);
  updateCellStyles();

  const er = document.getElementById("erases");
  if (er && data.erases !== undefined) er.innerText = `${data.erases}/3`;
}

/**
 * Actualiza las celdas del tablero de Sudoku.
 *
 * Itera sobre el tablero de Sudoku y actualiza los estilos de las celdas
 * según se hayan fijado o no.
 *
 * - Las celdas fijas se marcan con un fondo gris y un cursor por defecto.
 * - Las celdas no fijas se marcan con un fondo gris claro en hover.
 *
 * Luego, llama a la función updateCellStyles() para actualizar los estilos
 * de las celdas.
 */
function updateBoardVisual(board, fixed = null) {
  if (!board) return;

  for (let i = 0; i < 9; i++) {
    for (let j = 0; j < 9; j++) {
      const btn = document.getElementById(`${i}-${j}`);
      if (!btn) continue;

      const val = board[i][j];
      btn.innerText = val === 0 ? "" : String(val);

      if (fixed) {
        btn.dataset.fixed = fixed[i][j] ? "1" : "0";
      }

      if (btn.dataset.fixed === "1") {
        btn.classList.add("bg-gray-200", "cursor-default");
        btn.classList.remove(
          "hover:bg-gray-300",
          "cursor-pointer",
          "bg-gray-400"
        );
      } else {
        btn.classList.remove("bg-gray-200", "cursor-default", "bg-gray-400");
        btn.classList.add("hover:bg-gray-300", "cursor-pointer");
      }
    }
  }

  updateCellStyles();
}

/**
 * Muestra un mensaje de felicitación cuando se completa el Sudoku.
 *
 * Esta función se llama automáticamente cuando se completa el Sudoku.
 */
function winner() {
  alert("¡Felicidades! Completaste el Sudoku.");
}