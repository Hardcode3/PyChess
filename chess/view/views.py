import pygame
from settings import Settings, Colors, Fonts
from chess.pygame_toolkit.menus import Menu
from chess.pygame_toolkit.label import Label
from chess.pygame_toolkit.button import PushButton


class SplashScreen(Menu):
    def __init__(self, display: pygame.Surface) -> None:
        super().__init__(display)
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.1,
                Fonts.COMIC_SANS_MS_BOLD,
                80,
                Colors.BLACK,
                "Chess",
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.3,
                Fonts.COMIC_SANS_MS_BOLD,
                50,
                "play",
                Colors.BLACK,
                Colors.GREEN,
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.4,
                Fonts.COMIC_SANS_MS_BOLD,
                50,
                "new game",
                Colors.BLACK,
                Colors.RED,
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.5,
                Fonts.COMIC_SANS_MS_BOLD,
                50,
                "saves",
                Colors.BLACK,
                Colors.GREEN,
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.6,
                Fonts.COMIC_SANS_MS_BOLD,
                50,
                "settings",
                Colors.BLACK,
                Colors.GREEN,
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.8,
                Fonts.COMIC_SANS_MS,
                40,
                "quit",
                Colors.BLACK,
                Colors.GREEN,
            )
        )


class SettingsMenu(Menu):
    def __init__(self, display: pygame.Surface) -> None:
        super().__init__(display)
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.1,
                Fonts.COMIC_SANS_MS_BOLD,
                70,
                Colors.BLACK,
                "settings",
            )
        )
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE * 0.3,
                Settings.WINDOW_SIZE * 0.3,
                Fonts.COMIC_SANS_MS,
                30,
                Colors.BLACK,
                "Threads: ",
            )
        )
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE * 0.3,
                Settings.WINDOW_SIZE * 0.4,
                Fonts.COMIC_SANS_MS,
                30,
                Colors.BLACK,
                "Hash: ",
            )
        )
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE * 0.3,
                Settings.WINDOW_SIZE * 0.5,
                Fonts.COMIC_SANS_MS,
                30,
                Colors.BLACK,
                "Skill level: ",
            )
        )
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE * 0.3,
                Settings.WINDOW_SIZE * 0.6,
                Fonts.COMIC_SANS_MS,
                30,
                Colors.BLACK,
                "Depth: ",
            )
        )
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE * 0.3,
                Settings.WINDOW_SIZE * 0.7,
                Fonts.COMIC_SANS_MS,
                30,
                Colors.BLACK,
                "Minimum thinking time: ",
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.9,
                Fonts.COMIC_SANS_MS,
                40,
                "back to main menu",
                Colors.BLACK,
                Colors.GREEN,
            )
        )


class SaveMenu(Menu):
    def __init__(self, display: pygame.Surface) -> None:
        super().__init__(display)
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.1,
                Fonts.COMIC_SANS_MS_BOLD,
                70,
                Colors.BLACK,
                "saves",
            )
        )
        # first save
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE * 0.2,
                Settings.WINDOW_SIZE * 0.3,
                Fonts.COMIC_SANS_MS,
                35,
                Colors.BLACK,
                "save 1: ",
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE * 0.45,
                Settings.WINDOW_SIZE * 0.3,
                Fonts.COMIC_SANS_MS,
                35,
                "load",
                Colors.BLACK,
                Colors.GREEN,
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE * 0.75,
                Settings.WINDOW_SIZE * 0.3,
                Fonts.COMIC_SANS_MS,
                35,
                "overwrite",
                Colors.BLACK,
                Colors.RED,
            )
        )
        # second save
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE * 0.2,
                Settings.WINDOW_SIZE * 0.4,
                Fonts.COMIC_SANS_MS,
                35,
                Colors.BLACK,
                "save 2: ",
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE * 0.45,
                Settings.WINDOW_SIZE * 0.4,
                Fonts.COMIC_SANS_MS,
                35,
                "load",
                Colors.BLACK,
                Colors.GREEN,
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE * 0.75,
                Settings.WINDOW_SIZE * 0.4,
                Fonts.COMIC_SANS_MS,
                35,
                "overwrite",
                Colors.BLACK,
                Colors.RED,
            )
        )
        # third save
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE * 0.2,
                Settings.WINDOW_SIZE * 0.5,
                Fonts.COMIC_SANS_MS,
                35,
                Colors.BLACK,
                "save 3: ",
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE * 0.45,
                Settings.WINDOW_SIZE * 0.5,
                Fonts.COMIC_SANS_MS,
                35,
                "load",
                Colors.BLACK,
                Colors.GREEN,
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE * 0.75,
                Settings.WINDOW_SIZE * 0.5,
                Fonts.COMIC_SANS_MS,
                35,
                "overwrite",
                Colors.BLACK,
                Colors.RED,
            )
        )
        # fourth save
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE * 0.2,
                Settings.WINDOW_SIZE * 0.6,
                Fonts.COMIC_SANS_MS,
                35,
                Colors.BLACK,
                "save 4: ",
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE * 0.45,
                Settings.WINDOW_SIZE * 0.6,
                Fonts.COMIC_SANS_MS,
                35,
                "load",
                Colors.BLACK,
                Colors.GREEN,
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE * 0.75,
                Settings.WINDOW_SIZE * 0.6,
                Fonts.COMIC_SANS_MS,
                35,
                "overwrite",
                Colors.BLACK,
                Colors.RED,
            )
        )

        # back to main menu
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.8,
                Fonts.COMIC_SANS_MS,
                40,
                "back to main menu",
                Colors.BLACK,
                Colors.GREEN,
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.9,
                Fonts.COMIC_SANS_MS,
                25,
                "reset all saves",
                Colors.BLACK,
                Colors.RED,
            )
        )
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.2,
                Fonts.COMIC_SANS_MS,
                15,
                Colors.BLACK,
                "saves in source_dir/chess/saves/*.txt",
            )
        )


class EndGameMenu(Menu):
    def __init__(self, display: pygame.Surface) -> None:
        super().__init__(display)

        self.add_entity(
            Label(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.2,
                Fonts.COMIC_SANS_MS_BOLD,
                50,
                Colors.BLACK,
                "-",
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.5,
                Fonts.COMIC_SANS_MS,
                35,
                "save a log of the game",
                Colors.BLACK,
                Colors.GREEN,
            )
        )
        self.add_entity(
            Label(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.55,
                Fonts.COMIC_SANS_MS,
                15,
                Colors.BLACK,
                "the log will be saved under chess/logs",
            )
        )
        self.add_entity(
            PushButton(
                Settings.WINDOW_SIZE / 2,
                Settings.WINDOW_SIZE * 0.8,
                Fonts.COMIC_SANS_MS,
                40,
                "back to main menu",
                Colors.BLACK,
                Colors.GREEN,
            )
        )


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((Settings.WINDOW_SIZE, Settings.WINDOW_SIZE))
    SplashScreenTest = SplashScreen(display)
    SplashScreenTest.run()
