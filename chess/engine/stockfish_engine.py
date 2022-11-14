# -*- coding:utf-8 -*-
__projet__ = "Chess"
__nom_fichier__ = "stockfish"
__author__ = "PENOT Baptiste"
__date__ = "août 2022"

import os
from stockfish import Stockfish
from settings import Directories


def stockfish_test():
    """
    A simple test function for the stockfish package.
    """
    engine = Stockfish(Directories.STOCKFISH_DIR)
    engine.make_moves_from_current_position(["a2a4"])
    print(engine.get_board_visual())
    # print(engine.is_move_correct("a2a3"))
    # print(engine.get_board_visual())
    # print(engine.make_moves_from_current_position(["a2a4"]))
    # print(engine.get_board_visual())
    print(engine.get_top_moves(5))
    # print(engine.get_wdl_stats())
    # print(engine.get_parameters())
    # print(engine.get_fen_position())


if __name__ == '__main__':
    stockfish_test()
