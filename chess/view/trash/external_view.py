from settings import Settings
import pygame
import stockfish


def draw_deleted_pawns(display: pygame.Surface, chess_engine: stockfish.Stockfish):
    """
    Draw the deleted paws on the side of the window as the game goes on.
    """
    oponent_player = pygame.draw.rect(display, Settings.DELETED_PAWNS_SURFACE_COLOR,
                                      pygame.Rect(
                                          Settings.DELETED_PAWNS_OPONENT_POS[0],
                                          Settings.DELETED_PAWNS_OPONENT_POS[1],
                                          Settings.DELETED_PAWNS_SIZE * 16,
                                          Settings.DELETED_PAWNS_SIZE))
    me_player = pygame.draw.rect(display, Settings.DELETED_PAWNS_SURFACE_COLOR,
                                 pygame.Rect(
                                     Settings.DELETED_PAWNS_ME_POS[0],
                                     Settings.DELETED_PAWNS_ME_POS[1],
                                     Settings.DELETED_PAWNS_SIZE * 16,
                                     Settings.DELETED_PAWNS_SIZE))

