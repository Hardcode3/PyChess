import pygame
import stockfish
from settings import Settings, Colors, Fonts
from chess.pygame_toolkit.menus import Menu
from chess.pygame_toolkit.button import PushButton, CheckBox
from chess.pygame_toolkit.label import Label


class MainMenu(Menu):
    def __init__(self, display: pygame.Surface, buttons=None, labels=None, images=None, checkboxes=None,
                 background_color=Colors.WHITE):
        super().__init__(display, buttons=buttons, labels=labels, images=images, checkboxes=checkboxes,
                         background_color=background_color)

    def run(self, run: bool):
        while run:
            mouse_position = pygame.mouse.get_pos()
            right_mouse_click = pygame.mouse.get_pressed()[0]
            self.display_.fill(self.background_color_)
            events = pygame.event.get() + [pygame.event.wait()]
            self.event_handler(events)
            self.update_objects(mouse_position, right_mouse_click)
            pygame.display.update()
        pygame.quit()
        exit()


class SettingsMenu(Menu):
    def __init__(self, display: pygame.Surface, buttons=None, labels=None, images=None, checkboxes=None,
                 background_color=Colors.WHITE):
        super().__init__(display, buttons=buttons, labels=labels, images=images, checkboxes=checkboxes,
                         background_color=background_color)


class EndMenu(Menu):
    def __init__(self, display: pygame.Surface, buttons=None, labels=None, images=None, checkboxes=None,
                 background_color=Colors.LIGHT_YELLOW):
        super().__init__(display, buttons=buttons, labels=labels, images=images, checkboxes=checkboxes,
                         background_color=background_color)


def view_handling(display: pygame.Surface, engine: stockfish.Stockfish):
    main_menu(display)


def close():
    print("close")
    pygame.quit()
    exit()





def main_menu(display: pygame.Surface):
    MenuStatus.MAIN_MENU_RUN = True
    print("main menu")
    main_title = Label(int(Settings.WINDOW_SIZE * .5),
                       int(Settings.WINDOW_SIZE * .1),
                       Fonts.HERCULANUM,
                       60,
                       Colors.BLACK,
                       "MAIN MENU")
    play_button = PushButton(int(Settings.WINDOW_SIZE * .5),
                             int(Settings.WINDOW_SIZE * .35),
                             Fonts.HERCULANUM,
                             50,
                             "PLAY",
                             Colors.BLACK,
                             Colors.GREEN,
                             [[end_main_menu, None]])
    save_button = PushButton(int(Settings.WINDOW_SIZE * .5),
                             int(Settings.WINDOW_SIZE * .5),
                             Fonts.HERCULANUM,
                             50,
                             "SAVE",
                             Colors.BLACK,
                             Colors.GREEN)
    options_button = PushButton(int(Settings.WINDOW_SIZE * .5),
                                int(Settings.WINDOW_SIZE * .65),
                                Fonts.HERCULANUM,
                                50,
                                "OPTIONS",
                                Colors.BLACK,
                                Colors.GREEN,
                                [[settings_menu, display]])
    quit_button = PushButton(int(Settings.WINDOW_SIZE * .5),
                             int(Settings.WINDOW_SIZE * .9),
                             Fonts.HERCULANUM,
                             50,
                             "quit",
                             Colors.BLACK,
                             Colors.RED,
                             [[close, None]])

    MainMenu(display,
             {"play": play_button, "save": save_button, "options": options_button, "quit": quit_button},
             {"main title": main_title},
             {}).run(MenuStatus.MAIN_MENU_RUN)


def settings_menu(display: pygame.Surface):
    MenuStatus.MENU_SETTINGS_RUN = True
    print("main menu")
    main_title = Label(int(Settings.WINDOW_SIZE * .5),
                       int(Settings.WINDOW_SIZE * .1),
                       Fonts.HERCULANUM,
                       60,
                       Colors.BLACK,
                       "SETTINGS")
    back_button = PushButton(int(Settings.WINDOW_SIZE * .5),
                             int(Settings.WINDOW_SIZE * .9),
                             Fonts.HERCULANUM,
                             50,
                             "back",
                             Colors.BLACK,
                             Colors.GREEN,
                             [[end_settings, None]])
    checkbox = CheckBox(int(Settings.WINDOW_SIZE / 4),
                        int(Settings.WINDOW_SIZE / 5),
                        30,
                        False,
                        Colors.BLACK,
                        Colors.GREEN,
                        line_width=4)
    Menu(display,
         {"quit": back_button},
         {"main title": main_title},
         {},
         {"checkbox": checkbox}).run(MenuStatus.MENU_SETTINGS_RUN)
