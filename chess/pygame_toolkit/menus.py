import sys

import pygame
from typing import Tuple
from settings import Colors, Fonts
from chess.pygame_toolkit.button import (
    Button,
    PushButton,
    CheckBox
)
from chess.pygame_toolkit.label import Label


class Menu:
    def __init__(self,
                 display: pygame.Surface,
                 entities=None,
                 background_color: Tuple[int, int, int] = Colors.WHITE):
        if isinstance(display, pygame.Surface):
            self.display_ = display
        else:
            raise TypeError("display has to be a pygame.Surface")
        if isinstance(background_color, tuple):
            self.background_color_ = background_color
        else:
            raise TypeError("background color should be a tuple of 3 integers (RGB)")
        if not isinstance(entities, list):
            self.entities_ = []
        else:
            self.entities_ = entities
        self.run_ = True

    def get_entities(self):
        return self.entities_

    def get_entity(self, index: int) -> Label | Button | PushButton | CheckBox:
        if 0 <= index <= len(self.entities_) - 1:
            return self.entities_[index]
        raise RuntimeError("Index out of bounds for entities container")

    def add_entity(self, entity: Label | Button | PushButton | CheckBox) -> None:
        self.entities_.append(entity)

    def remove_entity(self, index: int) -> None:
        if 0 <= index <= len(self.entities_) - 1:
            self.entities_.remove(index)

    def run(self):
        while self.run_:
            self.display_.fill(self.background_color_)
            events = pygame.event.get() + [pygame.event.wait()]
            self.event_handler(events)
            self.render()
            pygame.display.update()
        pygame.quit()
        sys.exit()

    def render(self):
        for entity in self.entities_:
            entity.render(self.display_)

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.run_ = False


def print_message(message: str = "message") -> None:
    print(message)


if __name__ == '__main__':
    pygame.init()
    display = pygame.display.set_mode((600, 600))
    TestMenu = Menu(display, [
        Button(50, 50, Fonts.COMIC_SANS_MS, 35, "ouais", Colors.BLACK, Colors.PURPLE, Colors.RED,
               [[print_message, "ButtonClicked"]])
    ])
    TestMenu.add_entity(CheckBox(500, 400, 40, True, Colors.BLACK, Colors.RED, Colors.PURPLE, line_width=10,
                                 callbacks=[[print_message, "CheckBoxClicked !"]]))
    TestMenu.add_entity(
        PushButton(40, 300, Fonts.COMIC_SANS_MS_BOLD, 20, "PushButton", Colors.RED, Colors.BLACK,
                   [[print_message, "PushButtonClicked"]]))
    TestMenu.run()
