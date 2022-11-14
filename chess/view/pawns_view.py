# -*- coding:utf-8 -*-
__projet__ = "Chess"
__nom_fichier__ = "draw_pawns"
__author__ = "PENOT Baptiste"
__date__ = "août 2022"

import pygame
from chess.engine.fen import ForsythEdwardsNotation
from assets.pieces.pieces import get_piece_path
from settings import Settings


def draw_pieces(board: pygame.Surface, fen: str) -> None:
    """
    Draw all the pieces on the chess board using the fen notation.
    :param board: a surface in pygame
    :param fen: the fen notation
    """
    # extracting the board from the FEN notation
    piece_pattern = ForsythEdwardsNotation(fen).board
    for j in range(8):
        for i in range(8):
            if piece_pattern[j][i] != "1":
                draw_piece(board,
                           (Settings.CELL_GAP + i * Settings.CELL_SIZE, Settings.CELL_GAP + j * Settings.CELL_SIZE),
                           piece_pattern[j][i])


def draw_piece(board: pygame.Surface, position: tuple, piece_name: str) -> None:
    """
    Draw a pawn on a surface using its name in the FEN notation and its position.
    :param board: the pygame surface to draw on
    :param position: the position of the piece (top left corner)
    :param piece_name: the name of the piece in the FEN notation
    """
    pawn_raster = pygame.image.load(get_piece_path(piece_name)).convert_alpha()
    pawn = pygame.transform.scale(pawn_raster, (Settings.PAWN_SIZE, Settings.PAWN_SIZE))
    board.blit(pawn, position)
