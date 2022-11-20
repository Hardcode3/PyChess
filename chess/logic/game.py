"""
@file game.py
@brief Handles the logic of the game, including all the interactions between views and use input
"""

import os.path
import time
from typing import Tuple
from random import randint
import pygame.display
from stockfish import Stockfish
from setup import compile_stockfish
from pygame.locals import MOUSEBUTTONDOWN, K_r, K_q, K_ESCAPE
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
from chess.view.views import SplashScreen, SettingsMenu, SaveMenu, EndGameMenu
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

        self.log_: str = ""

        # setting up the different views of the game
        self.splash_screen_view_ = SplashScreen(self.display_)
        self.settings_screen_view_ = SettingsMenu(self.display_)
        self.save_screen_view_ = SaveMenu(self.display_)
        self.end_game_view_ = EndGameMenu(self.display_)
        self.saves_ = [
            Save(f"save_{i}.txt", absolute_path=False)
            for i in range(Settings.SAVE_NUMBER)
        ]
        self.configure_engine_parameters()
        self.configure_callbacks()
        self.splash_screen_view_.run()

    def configure_engine_parameters(self) -> None:
        """
        @brief Creates a parameter file if it does not exists, otherwise load it for the game
        """
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

        # end game screen
        self.end_game_view_.get_entity(1).set_callback(self.export_log)
        self.end_game_view_.get_entity(3).set_callback(self.splash_screen_view_.run)

    def run_game(self) -> None:
        """
        This method the main loop of the game, event driven.
        """
        while self.run_:
            for event in pygame.event.get() + [pygame.event.wait()]:
                keyboard_input = pygame.key.get_pressed()

                if event.type == pygame.QUIT or keyboard_input[K_q]:
                    self.close()

                if keyboard_input[K_r]:
                    self.game_engine_.set_position()
                    self.draw()

                if keyboard_input[K_ESCAPE]:
                    self.playing_ = False
                    self.splash_screen_view_.run()

                else:
                    if not self.playing_:
                        self.draw()
                        self.playing_ = True

                    if event.type == MOUSEBUTTONDOWN and not self.selection_:
                        self.draw(legal_moves=True)

                    elif event.type == MOUSEBUTTONDOWN and self.selection_:
                        self.move()
                        self.opponent_play()
                        self.endgame()

                    pygame.display.update()
                    self.update_views_objects()

    def close(self) -> None:
        """
        @brief Saves and closes the game
        Saves stockfish engine parameters, quit pygame and the current process
        """
        self.save_engine_parameters()
        pygame.quit()
        exit()

    def export_log(self) -> None:
        """
        @brief writes the log of the current game in a new text file located in chess/logs
        """
        date_n_time = time.ctime().replace(" ", "-").replace(":", "_")
        with open(os.path.join(Directories.LOGS, f"log_{date_n_time}.txt"), "w") as log:
            log.write(self.log_)

    def save(self, save_index: int) -> None:
        """
        @brief Saves the current game indicated by the fen notation in text files
        @see fen.py
        """
        if 0 <= save_index <= Settings.SAVE_NUMBER:
            self.saves_[save_index].write_save(self.game_engine_.get_fen_position())
        else:
            raise ValueError(
                f"Save index {save_index} is out of bounds [0, {Settings.SAVE_NUMBER}]"
            )

    def load_save(self, save_index: int) -> None:
        """
        @brief Loads game saves from save files
        @see save.py
        Saves are located in chess/save
        """
        if 0 <= save_index <= Settings.SAVE_NUMBER:
            save = self.saves_[save_index].load_save()
            if self.game_engine_.is_fen_valid(save):
                self.game_engine_.set_fen_position(save)
            else:
                print(
                    f"Error loading the fen which is not valid, replacing it with the default fen"
                )
                self.game_engine_.set_fen_position(Settings.FEN_POSITION_BEGIN)
            self.run_game()
        else:
            raise ValueError(
                f"Save index {save_index} is out of bounds [0, {Settings.SAVE_NUMBER}]"
            )

    def save_engine_parameters(self) -> None:
        """
        @brief Saves the parameters of stockfish in an appropriate text file
        @see engine_params.txt
        """
        self.configure_engine_parameters()
        with open(Directories.ENGINE_SAVE_PATH, "w") as fs:
            fs.write(str(self.game_engine_.get_parameters()))

    def load_engine_parameters(self) -> None:
        """
        @brief loads the parameters of stockfish in the engine_params.txt file
        """
        with open(Directories.ENGINE_SAVE_PATH, "r") as fs:
            params = eval(fs.read())
            self.game_engine_.update_engine_parameters(params)

    def set_engine_param_to(self, engine_param: str, value: int | str) -> None:
        """
        @brief sets stockfish parameters using its name as a string and the value it should overwrite
        @param engine_param the parameters of the engine in a string that should see its value modified
        @param value the new engine parameter as a string, integer of float
        """
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
        """
        @brief creates a new game by setting the fen to default
        Also launches the game view afterward
        """
        self.game_engine_.set_fen_position(Settings.FEN_POSITION_BEGIN)
        self.run_game()

    def reset_saves(self) -> None:
        """
        @brief ereases all the saves with the default one making them start from the begining
        """
        for elt in self.saves_:
            elt.write_save(Settings.FEN_POSITION_BEGIN)

    def reset(self) -> None:
        """
        @brief sets the background color to white hence erasing all former content
        """
        self.display_.fill(Settings.BG_COLOR)

    def draw(self, legal_moves: bool = False, time_to_wait: float = 0) -> None:
        """
        @brief draws the contour, the board and the pieces considering the fen notation of the engine
        @param legal_moves if true, draw dots indicators in the chessboard cells highlighting the legal moves player can do
        @param time_to_wait a delayer between the stockfish engine and the player (if zero, stockfish may play as soon as the mouse is clicked)
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
        @param move a piece based on the selection
        """
        selected = find_cell_from_mouse_pos(pygame.mouse.get_pos())
        if selected in get_legal_moves(self.game_engine_, self.selection_):
            move = f"{convert_datum(self.selection_)}{convert_datum(selected)}"
            self.game_engine_.make_moves_from_current_position([move])
            self.log_ += f"{str(move)}\n"
            play_sound(slide_sound=True)
            # write the log file here
        self.turn()
        self.selection_ = None
        self.draw()

    def opponent_play(self):
        """
        @brief oponent can be you, clicking other pawns, or stockfish and this method handles it
        """
        if Settings.IS_COMPUTER_OPPONENT and not self._is_white_turn:
            top_moves: list = self.game_engine_.get_top_moves(Settings.TOP_MOVES_NUMBER)
            opponent_play = top_moves[0]["Move"]
            self.game_engine_.make_moves_from_current_position([opponent_play])
            self.log_ += f"{str(opponent_play)}\n"
            play_sound(slide_sound=True)
        self.draw(time_to_wait=1)

    def half_move_clock(self) -> None:
        """
        @brief exits the game if the half_move clock is reached
        Whenever the number of half-moves reaches 50, the game is stale mate
        """
        if (
            ForsythEdwardsNotation(self.game_engine_.get_fen_position()).half_move_clock
            == 50
        ):
            self.end_game_view_.get_entity(0).set_text("stale mate...")
            self.end_game_view_.run()

    def check_for_mate(self) -> None:
        """
        @brief checks if a player is mate hence ending the current game
        """
        eval = self.game_engine_.get_evaluation()
        print(eval)
        if eval["type"] == "mate":
            if eval["value"] == -1:
                print("WHITE ARE CKECKMATE")
                self.end_game_view_.get_entity(0).set_text("black won !")
                self.end_game_view_.run()
            elif eval["value"] == 1:
                print("BLACK ARE CHECKMATE")
                self.end_game_view_.get_entity(0).set_text("white won !")
                self.end_game_view_.run()
            else:
                pass
                # no mate

    def endgame(self) -> None:
        self.check_for_mate()
        # self.half_move_clock()

    def update_views_objects(self) -> None:
        """
        @brief checks if the label in the splash screen should be displaying new game or not depending on the FEN satus
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
        @brief set the turn as a boolean by modifying the respective attribute
        """
        fen = ForsythEdwardsNotation(self.game_engine_.get_fen_position()).active_color
        if fen == "b":
            self._is_white_turn = False
        else:
            self._is_white_turn = True

    def delayer(self, time_to_wait: float) -> None:
        """
        @brief event driven game hardly support the wait functions of the time and of the pygame.time libraries
        @param time_to_wait: the time to wait before executing the next lines of code
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
