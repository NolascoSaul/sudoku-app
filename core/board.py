import random

def generate_sudoku_board() -> list:
    """Genera un nuevo tablero de Sudoku aleatoriamente desde un archivo de texto.

    La función selecciona un archivo de texto aleatoriamente desde los archivos
    static/assets/board1.txt hasta static/assets/board10.txt y devuelve el tablero de
    Sudoku contenido en ese archivo.

    Returns:
    list: Un nuevo tablero de Sudoku generado aleatoriamente.
    """
    idx = random.randint(1, 10)
    return get_board_from_file(idx)

def get_board_from_file(index: int) -> list:
    """Lee un archivo de texto que contiene un tablero de Sudoku y devuelve un nuevo tablero generado desde ese archivo.
    
    Parameters:
    index (int): El índice del archivo de texto que se desea leer.
    
    Returns:
    list: Un nuevo tablero de Sudoku generado desde el archivo de texto.
    """
    board = []
    with open(f'./static/assets/board{index}.txt') as file:
        for line in file:
            if not line:
                break
            else:
                row = list(map(int, line.split()))
            board.append(row)

    file.close()
    return board

def reset_board() -> list:
    """Resetea el tablero de Sudoku actual y devuelve un nuevo tablero generado aleatoriamente.
    
    Devuelve un nuevo tablero de Sudoku generado aleatoriamente.
    """

    return generate_sudoku_board()

def check_move(board, row, col, num) -> tuple[bool, str | None]:
    
    """Comprueba si un movimiento de Sudoku es válido en un tablero.
    
    Devuelve un par de valores. El primer valor es un booleano que indica si el movimiento es válido o no.
    El segundo valor es un string que contiene el mensaje de error si el movimiento no es válido.
    Si el movimiento es válido, el segundo valor es None.
    
    Parameters:
    board (list): El tablero de Sudoku.
    row (int): El índice de la fila en la que se desea hacer el movimiento.
    col (int): El índice de la columna en la que se desea hacer el movimiento.
    num (int): El número que se desea colocar en la celda.

    Returns:
    tuple: Un par de valores que indica si el movimiento es válido o no, y un mensaje de error en caso de que no sea válido."""
    if board[row][col] != 0:
        return False, "Celda ocupada"
    
    # Revisar fila
    if num in board[row]:
        return False, "Número repetido en fila"
    
    # Revisar columna
    if num in [board[row][col] for row in range(9)]:
        return False, "Número repetido en columna"
    
    # Revisar cuadrante
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False, "Número repetido en bloque"
    
    # Si pasa todas las comprobaciones
    board[row][col] = num
    return True, None

def check_win(board) -> bool:
    """Comprueba si un tablero de Sudoku ha sido ganado.
    
    Devuelve un booleano que indica si el tablero ha sido ganado o no.
    
    Parameters:
    board (list): El tablero de Sudoku.
    
    Returns:
    bool: Un booleano que indica si el tablero ha sido ganado o no."""
    for row in board:
        if 0 in row:
            return False
    return True