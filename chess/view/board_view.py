# -*- coding:utf-8 -*-
__projet__ = "Chess"
__nom_fichier__ = "draw_board"
__author__ = "PENOT Baptiste"
__date__ = "août 2022"

from typing import Tuple
from settings import (
    Settings,
    Colors
)
import pygame
from pygame.surface import Surface
from chess.engine.fen import ForsythEdwardsNotation, get_legal_moves
import stockfish


def draw_contour(display: Surface) -> None:
    """
    Draw a thin outer border for the chess board on a surface.
    :param display: the surface or display entity
    """
    contour = pygame.Surface((
        Settings.CHESS_BOARD_SIZE + 2 * Settings.BORDER_SIZE,
        Settings.CHESS_BOARD_SIZE + 2 * Settings.BORDER_SIZE))
    pygame.draw.rect(
        contour,
        Settings.BORDER_COLOR,
        pygame.Rect(0, 0,
                    Settings.CHESS_BOARD_SIZE + Settings.BORDER_SIZE,
                    Settings.CHESS_BOARD_SIZE + Settings.BORDER_SIZE))
    # pygame.draw.rect(
    #     contour,
    #     Colors.WHITE,
    #     pygame.Rect(Settings.BORDER_SIZE, Settings.BORDER_SIZE,
    #                 Settings.CHESS_BOARD_SIZE,
    #                 Settings.CHESS_BOARD_SIZE))
    display.blit(contour,
                 (Settings.GAP - Settings.BORDER_SIZE,
                  Settings.GAP - Settings.BORDER_SIZE))


def draw_empty_board(display: Surface, highlight: None | Tuple[int, int] = None) -> pygame.Surface:
    """
    Draw the empty board on a surface.
    :param highlight: the cell position to highlight as a tuple of integers, or None if no highlight
    :param display: the surface or display entity
    """
    board = pygame.Surface((
        Settings.CHESS_BOARD_SIZE, Settings.CHESS_BOARD_SIZE))
    cell_color = True
    for j in range(8):
        for i in range(8):
            if cell_color:
                color = Settings.CELL_COLOR1
            else:
                color = Settings.CELL_COLOR2
            pygame.draw.rect(
                board,
                color,
                pygame.Rect(
                    i * Settings.CELL_SIZE,
                    j * Settings.CELL_SIZE,
                    Settings.CELL_SIZE,
                    Settings.CELL_SIZE))
            cell_color = not cell_color
        cell_color = not cell_color
    if highlight:
        highlight_cell(board, highlight[0], highlight[1])
    return board


def highlight_cell(board: Surface, x: int, y: int) -> None:
    """
    Draw a rectangle on a surface at given positions. The color is given by the Settings class
    :param board: the chess board surface
    :param x: the horizontal axis (value between 0 and 7): growing to the right
    :param y: the vertical axis (value between 0 and 7): growing to the bottom
    """
    pygame.draw.rect(board, Settings.HIGHLIGHT_COLOR,
                     pygame.Rect(x * Settings.CELL_SIZE, y * Settings.CELL_SIZE,
                                 Settings.CELL_SIZE,
                                 Settings.CELL_SIZE))


def blit_board(display: pygame.Surface, board: pygame.Surface) -> None:
    display.blit(board, (Settings.GAP, Settings.GAP))


def draw_legal_moves(board: pygame.Surface, chess_engine: stockfish.Stockfish, position: Tuple[int, int]) -> list:
    """
    Draw the legal moves on the board for a selected piece.
    :param position: the position of the considered piece
    :param chess_engine: the chess engine, to verify if the moves are allowed or not
    :param board: a pygame.Surface object, which is the chess board
    """
    legal_moves = get_legal_moves(chess_engine, position)
    for elt in legal_moves:
        x, y = elt
        dot_position: Tuple[int, int] = Settings.CELL_SIZE * (.5 + x), Settings.CELL_SIZE * (.5 + y)
        pygame.draw.circle(board, Settings.LEGAL_CELL_INDICATOR_COLOR, dot_position,
                           Settings.LEGAL_CELL_INDICATOR_RADIUS)
    return legal_moves
