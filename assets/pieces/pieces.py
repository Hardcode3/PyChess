# -*- coding:utf-8 -*-
__projet__ = "Chess"
__nom_fichier__ = "pieces"
__author__ = "PENOT Baptiste"
__date__ = "août 2022"

import os
from settings import Directories
from dataclasses import dataclass


@dataclass
class PiecesRaster:
    fen_name: str
    name: str
    img_file: str


class PiecesData:
    POSSIBLE_PIECES = ["r", "n", "b", "q", "k", "p", "R", "N", "B", "Q", "K", "P"]


# PIECES_PATH: str = os.path.join(Directories.ROOT_DIR, "assets/pieces/default")
PIECES_PATH: str = os.path.join(Directories.ROOT_DIR, "assets/pieces/simple")

PIECES_RASTER_DICT: dict = {
    "r": os.path.join(PIECES_PATH, "rb.png"),
    "n": os.path.join(PIECES_PATH, "nb.png"),
    "b": os.path.join(PIECES_PATH, "bb.png"),
    "q": os.path.join(PIECES_PATH, "qb.png"),
    "k": os.path.join(PIECES_PATH, "kb.png"),
    "p": os.path.join(PIECES_PATH, "pb.png"),
    "R": os.path.join(PIECES_PATH, "rw.png"),
    "N": os.path.join(PIECES_PATH, "nw.png"),
    "B": os.path.join(PIECES_PATH, "bw.png"),
    "Q": os.path.join(PIECES_PATH, "qw.png"),
    "K": os.path.join(PIECES_PATH, "kw.png"),
    "P": os.path.join(PIECES_PATH, "pw.png")
}


def get_piece_path(piece_name: str) -> str:
    """
    Get the path of the image for any specified pawn .
    :param piece_name: the name of the pawn in the FEN notation.
    """
    if piece_name not in PiecesData.POSSIBLE_PIECES:
        raise NameError(f"No piece has the name {piece_name}")
    return PIECES_RASTER_DICT[piece_name]

#
# pieces_real_names: dict = {
#     "r": "black rook",
#     "n": "black knight",
#     "b": "black bishop",
#     "q": "black queen",
#     "k": "black king",
#     "p": "black pawn",
#     "R": "white rook",
#     "N": "white knight",
#     "B": "white bishop",
#     "Q": "white queen",
#     "K": "white king",
#     "P": "white pawn"
# }
