import sys

import stockfish
from settings import Settings, Colors
import pygame

# CHESS directory
from chess.save.save import write_save, load_save, is_saved


def options(display: pygame.Surface) -> False:
    """
    Prints the option (or settings) display of the game to choose which settings to trick.
    """
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        display.fill(Colors.BLACK)
        OptionScreenAttributes.OPTION_TEXT.render(display)
        OptionScreenAttributes.OPTIONS_BACK.change_color(OPTIONS_MOUSE_POS)
        OptionScreenAttributes.OPTIONS_BACK.render(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OptionScreenAttributes.OPTIONS_BACK.is_clicked(OPTIONS_MOUSE_POS):
                    return False
        pygame.display.update()


def option_stockfish_parameters():
    pass


def end_screen(display: pygame.surface, game_engine: stockfish.Stockfish, white_won: bool = False) -> None:
    """
    Prints the end game menu with the option to redo another game.
    """

    while True:
        END_GAME_MOUSE_POS = pygame.mouse.get_pos()
        display.fill(Colors.BLACK)

        if white_won:
            EndScreenAttributes.WINNER_TEXT.set_text(Settings.END_SCREEN_TEXT_WIGHT_WINS)
        else:
            EndScreenAttributes.WINNER_TEXT.set_text(Settings.END_SCREEN_TEXT_BLACK_WINS)

        EndScreenAttributes.END_SCREEN_TEXT.render(display)
        EndScreenAttributes.WINNER_TEXT.render(display)

        EndScreenAttributes.END_SCREEN_MAIN_MENU.change_color(END_GAME_MOUSE_POS)
        EndScreenAttributes.END_SCREEN_MAIN_MENU.render(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EndScreenAttributes.END_SCREEN_MAIN_MENU.is_clicked(END_GAME_MOUSE_POS):
                    main_menu(display, game_engine)
        pygame.display.update()


def main_menu(display: pygame.surface, game_engine: stockfish.Stockfish) -> int:
    """
    Print the main menu to the display. There are three buttons: play, options and quit.
    """

    while True:
        display.fill(Colors.BLACK)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MainScreenAttributes.MAIN_TITLE.render(display)
        update_save_button(game_engine, MainScreenAttributes.SAVE_BUTTON)

        for button in MainScreenAttributes.BUTTONS_LIST:
            button.change_color(MENU_MOUSE_POS)
            button.render(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MainScreenAttributes.PLAY_BUTTON.is_clicked(MENU_MOUSE_POS):
                    return 0
                if MainScreenAttributes.SAVE_BUTTON.is_clicked(MENU_MOUSE_POS):
                    return 1
                if MainScreenAttributes.NEW_GAME_BUTTON.is_clicked(MENU_MOUSE_POS):
                    return 2
                if MainScreenAttributes.LOAD_SAVE_BUTTON.is_clicked(MENU_MOUSE_POS):
                    return 3
                if MainScreenAttributes.OPTIONS_BUTTON.is_clicked(MENU_MOUSE_POS):
                    options(display)
                if MainScreenAttributes.QUIT_BUTTON.is_clicked(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def splash_screens_handling(display: pygame.Surface, game_engine: stockfish.Stockfish) -> False:
    """
    Handles the behavior of the splash screens.
    """

    state = main_menu(display, game_engine)

    if state == 0:
        return False
    elif state == 1:
        write_save(game_engine.get_fen_position())
    elif state == 2:
        game_engine.set_fen_position(Settings.FEN_POSITION_BEGIN)
        return False
    elif state == 3:
        game_engine.set_fen_position(load_save())
        return False


def update_save_button(game_engine, save_button) -> None:
    if is_saved(load_save(), game_engine.get_fen_position()):
        save_button.set_text(Settings.SAVED_MAIN_TEXT)
    else:
        save_button.set_text(Settings.SAVE_MAIN_TEXT)
