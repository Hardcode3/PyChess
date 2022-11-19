import os.path
import time
from typing import Tuple
from random import randint
import pygame.display
from stockfish import Stockfish
from setup import compile_stockfish
from pygame.locals import MOUSEBUTTONDOWN, K_r, K_ESCAPE
from settings import Settings, Directories, Colors

# ASSETS directory
from assets.sounds.sounds import play_sound

# CHESS.ENGINE directory
from chess.engine.datum_change import convert_datum
from chess.engine.fen import get_legal_moves, ForsythEdwardsNotation

# CHESS.VIEW
from chess.view.board_view import (
    draw_contour,
    draw_empty_board,
    blit_board,
    draw_legal_moves,
)
from chess.view.input_handling import find_cell_from_mouse_pos, is_valid_selection
from chess.view.views import SplashScreen, SettingsMenu, SaveMenu
from chess.pygame_toolkit.menus import Menu
from chess.view.pawns_view import draw_pieces
from chess.save.save import Save


class Game:
    """
    Class managing the game (controller).
    This is where the main loops happen.
    """

    def __init__(self) -> None:
        pygame.init()
        self.run_ = True
        self.game_engine_ = Stockfish(path=str(Directories.STOCKFISH_EXECUTABLE))
        self.board_ = None
        self.selection_: None | Tuple[int, int] = None
        self._is_white_turn: bool = True
        self.playing_: bool = False

        self.display_ = pygame.display.set_mode(
            (Settings.WINDOW_SIZE, Settings.WINDOW_SIZE)
        )
        pygame.display.set_caption(Settings.WINDOW_TITLE)
        pygame.display.set_icon(
            pygame.image.load(
                os.path.join(Directories.ASSETS_DIR, "game_icon/game_icon.png")
            )
        )

        # setting up the different views of the game
        self.splash_screen_view_ = SplashScreen(self.display_)
        self.settings_screen_view_ = SettingsMenu(self.display_)
        self.save_screen_view_ = SaveMenu(self.display_)
        self.end_screen_view_ = Menu(self.display_)
        self.saves_ = [
            Save(f"save_{i}.txt", absolute_path=False)
            for i in range(Settings.SAVE_NUMBER)
        ]
        self.configure_engine_parameters()
        self.configure_callbacks()
        self.splash_screen_view_.run()

    def configure_engine_parameters(self) -> None:
        if not os.path.exists(Directories.ENGINE_SAVE_PATH):
            with open(Directories.ENGINE_SAVE_PATH, "w") as fs:
                fs.write(str(self.game_engine_.get_parameters()))
        else:
            self.load_engine_parameters()

    def configure_callbacks(self) -> None:
        """
        @brief configure the equivalent of signals and slots system
        """
        # splash screen
        self.splash_screen_view_.get_entity(1).set_callback(self.run_game)
        self.splash_screen_view_.get_entity(3).set_callback(self.save_screen_view_.run)
        self.splash_screen_view_.get_entity(2).set_callback(self.new_game)
        self.splash_screen_view_.get_entity(4).set_callback(
            self.settings_screen_view_.run
        )
        self.splash_screen_view_.get_entity(5).set_callback(self.close)
        # settings screen
        self.settings_screen_view_.get_entity(6).set_callback(
            self.splash_screen_view_.run
        )
        # save screen
        self.save_screen_view_.get_entity(2).set_callback(self.load_save, args=0)
        self.save_screen_view_.get_entity(3).set_callback(self.save, args=0)
        self.save_screen_view_.get_entity(5).set_callback(self.load_save, args=1)
        self.save_screen_view_.get_entity(6).set_callback(self.save, args=1)
        self.save_screen_view_.get_entity(8).set_callback(self.load_save, args=2)
        self.save_screen_view_.get_entity(9).set_callback(self.save, args=2)
        self.save_screen_view_.get_entity(11).set_callback(self.load_save, args=3)
        self.save_screen_view_.get_entity(12).set_callback(self.save, args=3)
        self.save_screen_view_.get_entity(13).set_callback(self.splash_screen_view_.run)
        self.save_screen_view_.get_entity(14).set_callback(self.reset_saves)

    def run_game(self) -> None:
        """
        This method the main loop of the game, event driven.
        """
        while self.run_:
            for event in pygame.event.get() + [pygame.event.wait()]:
                keyboard_input = pygame.key.get_pressed()

                self.update_views_objects()

                if event.type == pygame.QUIT:
                    self.close()

                if keyboard_input[K_r]:
                    self.game_engine_.set_position()
                    self.draw()

                if keyboard_input[K_ESCAPE]:
                    self.playing_ = False
                    self.splash_screen_view_.run()

                else:
                    self.end_game()
                    self.half_move_clock()

                    if not self.playing_:
                        self.draw()
                        self.playing_ = True

                    if event.type == MOUSEBUTTONDOWN and not self.selection_:
                        self.draw(legal_moves=True)

                    elif event.type == MOUSEBUTTONDOWN and self.selection_:
                        self.move()
                        self.opponent_play()

                    pygame.display.update()

    def close(self) -> None:
        self.save_engine_parameters()
        pygame.quit()
        exit()

    def save(self, save_index: int) -> None:
        if 0 <= save_index <= Settings.SAVE_NUMBER:
            self.saves_[save_index].write_save(self.game_engine_.get_fen_position())
        else:
            raise ValueError(
                f"Save index {save_index} is out of bounds [0, {Settings.SAVE_NUMBER}]"
            )

    def load_save(self, save_index: int) -> None:
        if 0 <= save_index <= Settings.SAVE_NUMBER:
            save = self.saves_[save_index].load_save()
            self.game_engine_.set_fen_position(save)
            self.run_game()
        else:
            raise ValueError(
                f"Save index {save_index} is out of bounds [0, {Settings.SAVE_NUMBER}]"
            )

    def save_engine_parameters(self) -> None:
        self.configure_engine_parameters()
        with open(Directories.ENGINE_SAVE_PATH, "w") as fs:
            fs.write(str(self.game_engine_.get_parameters()))

    def load_engine_parameters(self) -> None:
        with open(Directories.ENGINE_SAVE_PATH, "r") as fs:
            params = eval(fs.read())
            self.game_engine_.update_engine_parameters(params)

    def set_engine_param_to(self, engine_param: str, value: int | str) -> None:
        if (
            engine_param not in self.game_engine_.get_parameters().keys()
            and not isinstance(engine_param, str)
        ):
            raise ValueError(
                f"Engine parameter in set_engine_param has an incorrect value {engine_param}"
            )
        else:
            params = self.game_engine_.get_parameters()[engine_param] = value
            # self.game_engine_.update_engine_parameters(params)

    def new_game(self) -> None:
        self.game_engine_.set_fen_position(Settings.FEN_POSITION_BEGIN)
        self.run_game()

    def reset_saves(self) -> None:
        for elt in self.saves_:
            elt.write_save(Settings.FEN_POSITION_BEGIN)

    def reset(self) -> None:
        """
        Set the background color to white and so erase all former content.
        """
        self.display_.fill(Settings.BG_COLOR)

    def draw(self, legal_moves: bool = False, time_to_wait: float = 0) -> None:
        """
        Draw the contour, the board and the pieces on it considering the fen notation of the engine.
        """
        self.delayer(time_to_wait)
        self.reset()
        draw_contour(self.display_)
        self.board_ = draw_empty_board(self.display_)
        draw_pieces(self.board_, self.game_engine_.get_fen_position())
        # TODO draw_deleted_pawns(self.display_, self.game_engine_)
        if legal_moves:
            selected = find_cell_from_mouse_pos(pygame.mouse.get_pos())
            if is_valid_selection(self.game_engine_.get_fen_position(), selected):
                draw_legal_moves(self.board_, self.game_engine_, selected)
                self.selection_ = selected
                play_sound(select_sound=True)
        blit_board(self.display_, self.board_)
        pygame.display.update()

    def move(self) -> None:
        """
        Move a piece based on  the selection.
        """
        selected = find_cell_from_mouse_pos(pygame.mouse.get_pos())
        # print(f"selected: {selected}")
        if selected in get_legal_moves(self.game_engine_, self.selection_):
            # print(f"legal moves: {get_legal_moves(self.game_engine_, self.selection_)}")
            move = f"{convert_datum(self.selection_)}{convert_datum(selected)}"
            # print(f"move achieved: {move}")
            self.game_engine_.make_moves_from_current_position([move])
            play_sound(slide_sound=True)
        self.turn()
        self.selection_ = None
        self.draw()

    def opponent_play(self):
        """
        Play in response to the white player input.
        Play mode: against the computer or against another player.
        """
        if Settings.IS_COMPUTER_OPPONENT and not self._is_white_turn:
            top_moves: list = self.game_engine_.get_top_moves(Settings.TOP_MOVES_NUMBER)
            # randomize a number to give a chance to the player
            opponent_play = top_moves[randint(0, Settings.TOP_MOVES_NUMBER - 1)]["Move"]
            self.game_engine_.make_moves_from_current_position([opponent_play])
        self.draw(time_to_wait=1)

    def half_move_clock(self) -> None:
        """
        Exit the game if the half_move clock is reached.
        """
        if (
            ForsythEdwardsNotation(self.game_engine_.get_fen_position()).half_move_clock
            == 50
        ):
            self.run_ = False

    def end_game(self):
        pass

    def update_views_objects(self) -> None:
        """
        @brief Checks if the label in the splash screen should be displaying new game or not depending on the FEN satus
        """
        if self.game_engine_.get_fen_position() == Settings.FEN_POSITION_BEGIN:
            # about the play / resume button
            self.splash_screen_view_.get_entity(1).text = "play"
            # about the new game button
            self.splash_screen_view_.get_entity(2).text = "-"
            self.splash_screen_view_.get_entity(2).is_clickable = False
            self.splash_screen_view_.get_entity(2).hoover_color = Colors.BLACK
        else:
            # about the play / resume button
            self.splash_screen_view_.get_entity(1).text = "resume"
            # about the new game button
            self.splash_screen_view_.get_entity(2).text = "new game"
            self.splash_screen_view_.get_entity(2).is_clickable = True
            self.splash_screen_view_.get_entity(2).hoover_color = Colors.BLACK

    def turn(self) -> None:
        """
        Get the turn as a boolean by modifying the respective attribute
        """
        fen = ForsythEdwardsNotation(self.game_engine_.get_fen_position()).active_color
        if fen == "b":
            self._is_white_turn = False
        else:
            self._is_white_turn = True

    def delayer(self, time_to_wait: float) -> None:
        """
        Event driven game hardly support the wait functions of the time and of the pygame.time libraries
        :param time_to_wait: the time to wait before executing the next lines of code
        """
        if time_to_wait > 0:
            clock = pygame.time.Clock()
            start = time.time()
            timer = time.time()
            while timer - start <= time_to_wait:
                self.draw()
                clock.tick(1)
                timer = time.time()


if __name__ == "__main__":
    main_view = Game()
