from flask import Flask, render_template, jsonify, redirect, url_for, request
from core.board import generate_sudoku_board, check_move, reset_board, check_win

app = Flask(__name__)

current_board = generate_sudoku_board()
erases_used = 0
MAX_ERASES = 3

@app.route("/")
def home():
    """
    La ruta principal de la aplicación. Devuelve el tablero de Sudoku actual,
    las celdas fijas y el número de borrados utilizados.
    
    Parameters:
    
    Returns:
        render_template: una plantilla HTML que contiene el tablero de Sudoku,
        las celdas fijas y el número de borrados utilizados.
    """
    global current_board, erases_used
    fixed_cells = [[cell != 0 for cell in row] for row in current_board] # Celdas iniciales
    return render_template("index.html", board=current_board, fixed=fixed_cells, erases=erases_used, max_erases=MAX_ERASES)

@app.route("/insert", methods=["POST"])
def insert():
    """
    Realiza una petición POST a "/insert" con un objeto payload que contiene la fila, columna y número que se desea insertar en la celda seleccionada.
    
    Devuelve un objeto JSON que contiene los siguientes campos:
    - success (bool): true si la petición fue exitosa, false en caso contrario.
    - error (string): el mensaje de error en caso de que la petición falla.
    - board (list): el tablero de Sudoku actualizado.
    - win (bool): true si el tablero de Sudoku es un tablero ganador, false en caso contrario.
    """
    global current_board
    try:
        data = request.get_json(force=True)
        row = int(data.get("row"))
        col = int(data.get("col"))
        num = int(data.get("num"))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Datos inválidos"}), 400

    if not (0 <= row <= 8 and 0 <= col <= 8 and 1 <= num <= 9):
        return jsonify({"success": False, "error": "Valores fuera de rango"}), 400

    success, error = check_move(current_board, row, col, num)
    win = check_win(current_board)
    return jsonify({
        "success": success,
        "error": error,
        "board": current_board,
        "win": win
    })



@app.route("/erase", methods=["POST"])
def erase():
    """
    Realiza una petición POST a "/erase" con un objeto payload que contiene la fila y columna de la celda que se desea borrar.
    
    Devuelve un objeto JSON que contiene los siguientes campos:
    - success (bool): true si la petición fue exitosa, false en caso contrario.
    - error (string): el mensaje de error en caso de que la petición falla.
    - board (list): el tablero de Sudoku actualizado.
    - erases (int): el número de borrados utilizados.
    """

    global current_board, erases_used
    try:
        data = request.get_json(force=True)
        row = int(data.get("row"))
        col = int(data.get("col"))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Datos inválidos"}), 400

    if not (0 <= row <= 8 and 0 <= col <= 8):
        return jsonify({"success": False, "error": "Celda fuera de rango"}), 400

    if erases_used >= MAX_ERASES:
        return jsonify({"success": False, "message": "Límite de borrados alcanzado"}), 400

    erased = False
    if current_board[row][col] != 0:
        current_board[row][col] = 0
        erases_used += 1
        erased = True

    return jsonify({"success": erased, "board": current_board, "erases": erases_used})


@app.route("/reset", methods=["POST"])
def reset():
    """
    Reinicia el juego de Sudoku.
    
    Resetea el tablero de Sudoku actual y devuelve un nuevo tablero generado aleatoriamente.
    
    Devuelve un objeto JSON que contiene los siguientes campos:
    - success (bool): true si la petición fue exitosa, false en caso contrario.
    - board (list): el tablero de Sudoku actualizado.
    - erases (int): el número de borrados utilizados.
    - fixed (list): una lista de booleanos que indica si cada celda del tablero es fija o no.
    """
    global current_board, erases_used
    current_board = reset_board()
    erases_used = 0
    fixed_cells = [[cell != 0 for cell in row] for row in current_board]
    return jsonify({"success": True, "board": current_board, "erases": erases_used, "fixed": fixed_cells})

@app.errorhandler(404)
def not_found(error):
    """
    Maneja el error 404 redirigiendo a la página principal.
    
    Parameters:
    error - El objeto de error que se pasa a esta función.
    
    Returns:
    redirect - Una respuesta de redirección a la página principal.
    """
    return redirect(url_for("home"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)