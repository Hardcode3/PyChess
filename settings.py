# -*- coding:utf-8 -*-
__projet__ = "Chess"
__nom_fichier__ = "settings"
__author__ = "PENOT Baptiste"
__date__ = "août 2022"

import os
from dataclasses import dataclass
from typing import Tuple
import pygame


@dataclass
class Directories:
    ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR: str = os.path.join(ROOT_DIR, "assets")
    CHESS_DIR: str = os.path.join(ROOT_DIR, "chess")
    ENGINE_DIR: str = os.path.join(CHESS_DIR, "engine")
    SAVE_DIR: str = os.path.join(CHESS_DIR, "save")
    EXTERNAL_DEPS: str = os.path.join(CHESS_DIR, "external")

    UNIX_CONFIG_SCRIPT: str = os.path.join(EXTERNAL_DEPS, "unix_compile_stockfish.sh")
    STOCKFISH_DIR: str = os.path.join(EXTERNAL_DEPS, "Stockfish")
    STOCKFISH_MAKEFILE: str = os.path.join(os.path.join(STOCKFISH_DIR, "src/Makefile"))
    STOCKFISH_EXECUTABLE: str = os.path.join(STOCKFISH_DIR, "src/stockfish")

    ENGINE_SAVE_PATH = os.path.join(ENGINE_DIR, "engine_params.txt")


@dataclass
class Colors:
    """
    Dataclass containing the colors for pygame.
    """

    WHITE: tuple = (255, 255, 255)
    BLACK: tuple = (0, 0, 0)
    GREY: tuple = (169, 169, 169)
    BLUE: tuple = (0, 0, 255)
    RED: tuple = (241, 64, 70)
    GREEN: tuple = (118, 203, 70)
    PURPLE: tuple = (102, 0, 255)
    LIGHT_YELLOW: tuple = (240, 240, 128)
    LIGHT_GREY: tuple = (216, 216, 216)


@dataclass
class Settings:
    """
    Dataclass containing the settings of the project.
    """

    # game mode (by default, the computer plays automatically)
    IS_COMPUTER_OPPONENT: bool = True
    # the highest the top move's, the highest the chance for the bot to make errors
    TOP_MOVES_NUMBER: int = 4
    # time before drawing the next play on the screen [seconds]
    TIMER_BETWEEN_PLAYERS: int = 1

    # splash screen settings
    SPLASH_BACKGROUND_COLOR: tuple = Colors.WHITE

    # main window settings
    WINDOW_TITLE: str = "Chess"
    WINDOW_SIZE: int = 650
    GAP: int = WINDOW_SIZE / 10
    BORDER_SIZE: int = 5

    # chessboard settings
    CHESS_BOARD_SIZE: int = WINDOW_SIZE - 2 * GAP
    CELL_SIZE: int = CHESS_BOARD_SIZE / 8
    PAWN_SIZE: int = CELL_SIZE * 0.9
    CELL_GAP: int = (CELL_SIZE - PAWN_SIZE) / 2
    LEGAL_CELL_INDICATOR_RADIUS: int = 5

    # the deleted pawns have the following settings
    DELETED_PAWNS_ME_POS: tuple = 0.1 * WINDOW_SIZE, 0.9 * WINDOW_SIZE
    DELETED_PAWNS_OPONENT_POS: tuple = 0.1 * WINDOW_SIZE, 0.05 * WINDOW_SIZE
    DELETED_PAWNS_SIZE: int = 0.6 * CELL_SIZE
    DELETED_PAWNS_SURFACE_COLOR: Tuple[int, int, int] = Colors.LIGHT_GREY

    LEGAL_CELL_INDICATOR_COLOR: Tuple[int, int, int] = Colors.RED
    BORDER_COLOR: Tuple[int, int, int] = Colors.BLACK
    CELL_COLOR1: Tuple[int, int, int] = Colors.WHITE
    CELL_COLOR2: Tuple[int, int, int] = Colors.GREY
    BG_COLOR: Tuple[int, int, int] = Colors.WHITE
    HIGHLIGHT_COLOR: Tuple[int, int, int] = Colors.LIGHT_YELLOW

    # begin fen position
    FEN_POSITION_BEGIN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    # number of possible saves
    SAVE_NUMBER: int = 4


@dataclass
class GameConstants:
    LEFT_CLICK: int = 1
    RIGHT_CLICK: int = 3


@dataclass
class Fonts:
    pygame.font.init()
    Font = pygame.font.SysFont
    HERCULANUM: str = os.path.join(Directories.ASSETS_DIR, "fonts/Herculanum.ttf")
    COMIC_SANS_MS: str = os.path.join(Directories.ASSETS_DIR, "fonts/Comic Sans MS.ttf")
    COMIC_SANS_MS_BOLD: str = os.path.join(
        Directories.ASSETS_DIR, "fonts/Comic Sans MS Bold.ttf"
    )
