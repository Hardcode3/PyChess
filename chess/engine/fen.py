# -*- coding:utf-8 -*-
__projet__ = "Chess"
__nom_fichier__ = "fen"
__author__ = "PENOT Baptiste"
__date__ = "août 2022"

from typing import Tuple

import stockfish

from chess.engine.datum_change import convert_datum
from assets.pieces.pieces import PiecesData
from chess.engine.datum_change import DatumChange


def get_legal_moves(chess_engine: stockfish.Stockfish, position: tuple) -> list:
    valid_moves = []
    cell_id_t0: str = convert_datum(position)
    for elt in DatumChange.DATUM_CHANGE:
        move: str = f"{cell_id_t0}{elt[1]}"
        if chess_engine.is_move_correct(move):
            valid_moves.append(elt[0])
    return valid_moves


class ForsythEdwardsNotation:
    """
    A notation to save chess state.
    See https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    """

    def __init__(self, fen: str) -> None:
        self.fen_ = fen.split(" ")

    def is_fen_valid(self) -> bool:
        # todo
        return True

    @property
    def chess_state(self):
        return self.fen_[0]

    @property
    def active_color(self):
        return self.fen_[1]

    @property
    def castling_availability(self):
        return self.fen_[2]

    @property
    def en_passant_target(self):
        return self.fen_[3]

    @property
    def half_move_clock(self):
        return self.fen_[4]

    @property
    def full_move_number(self):
        return self.fen_[5]

    @property
    def board(self):
        board: list = []
        for row in self.chess_state.split("/"):
            temp_row = []
            for cell in row:
                if cell in [str(i) for i in range(1, 9)]:
                    for empty_cells in range(int(cell)):
                        temp_row.append('1')
                else:
                    temp_row.append(cell)
            board.append(temp_row)
        return board

    def get_pos_from_piece_name(self, piece_name: str) -> Tuple[Tuple[int, int], str] | None:
        """
        Get the position of any chess piece if exists, otherwise return None.
        :param piece_name: the name of the piece
        """
        if piece_name in PiecesData.POSSIBLE_PIECES:
            for j in range(8):
                for i in range(8):
                    if piece_name == self.board[j][i]:
                        return (i, j), convert_datum((i, j))


def test() -> bool:
    """
    A simple test function for the ForsythEdwardsNotation class.
    """
    print("--> Test of the ForsythEdwardsNotation class")
    fen = ForsythEdwardsNotation("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
    print(fen.chess_state)
    print(fen.active_color)
    print(fen.castling_availability)
    print(fen.en_passant_target)
    print(fen.half_move_clock)
    print(fen.full_move_number)
    print(fen.board)
    return True


if __name__ == '__main__':
    test()
