import sys
import pygame
import pygame_toolbox.graphics as ptg
from chess.view.screens_settings import (
    MainMenuSettings,
    OptionsMenuSettings,
    EndGameSettings
)
from settings import Settings, Colors


def close():
    pygame.quit()
    sys.exit()


class MainMenu(ptg.Menu):
    def __init__(self):
        ptg.Menu.__init__(self,
                          (Settings.WINDOW_SIZE, Settings.WINDOW_SIZE),
                          MainMenuSettings.BACKGROUND,
                          MainMenuSettings.MAIN_TITLE.TEXT,
                          []
                          )
        play_button = ptg.Button(
            0,
            MainMenuSettings.PLAY_BUTTON.TEXT,
            (MainMenuSettings.PLAY_BUTTON.POS_X, MainMenuSettings.PLAY_BUTTON.POS_Y),
            True,
            self.image
        )
        play_button.
        self.buttonlist.append(play_button)


class Main:
    def __init__(self):
        self.progress = 1
        self.clock = pygame.time.Clock()

    def update(self, screen):
        # Handle the events using a progress indicator and the update method of
        # the menu and text screen classes
        while True:
            if self.progress == 1:
                self.progress = MainMenu().update(screen, self.clock)
            elif self.progress == 2:
                close()


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    Main().update(screen)
