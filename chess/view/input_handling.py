"""
@file input_handling.py
@brief Defines functions to analyze user input
"""

from typing import Tuple
from settings import Settings
from chess.engine.fen import ForsythEdwardsNotation


def is_mouse_on_board(mouse_position: Tuple[int, int]) -> bool:
    """
    @brief returns True if the mouse position is over the chess board.
    @param mouse_position the mouse position as a tuple of two integers.
    """
    x, y = mouse_position
    if Settings.GAP < x < Settings.GAP + Settings.CHESS_BOARD_SIZE \
            and Settings.GAP < y < Settings.GAP + Settings.CHESS_BOARD_SIZE:
        return True
    return False


def find_cell_from_mouse_pos(mouse_position: Tuple[int, int]) -> Tuple[int, int] | None:
    """
    @brief gets the position of the mouse and returns the coordinates of the cell or None if the selection is not valid.
    @param mouse_position the mouse position as a tuple of two integers.
    """
    x, y = mouse_position
    if is_mouse_on_board(mouse_position):
        return int((x - Settings.GAP) / Settings.CELL_SIZE), int((y - Settings.GAP) / Settings.CELL_SIZE)


def is_valid_selection(fen: str, position: Tuple[int, int]) -> bool:
    """
    @brief checks is the selection is valid.
    A selection is valid whenever the player choose a populated cell.
    @param fen the fen notation describing the state of the game
    @param position cell's position (datum is top left)
    """
    if position is not None:
        x, y = position
        fen_ = ForsythEdwardsNotation(fen)
        cell = fen_.board[y][x]
        # if the fen is uppercase, then the selected pawn is white, and you can only play with white pawns
        if cell.isupper() and fen_.active_color == 'w' or cell.islower() and fen_.active_color == "b":
            return True
    return False
