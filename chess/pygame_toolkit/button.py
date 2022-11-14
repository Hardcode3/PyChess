import sys
from typing import (
    Tuple,
    Callable,
    List
)
import pygame
from settings import (
    Colors,
    Settings,
    Fonts
)
from chess.pygame_toolkit.label import Label


class Button(Label):
    # a delayer to eliminate close clicks (number of frame during which the button will be disabled)
    AFTER_CLICK_DELAYER: int = 10

    def __init__(self, x: int, y: int,
                 font: str,
                 font_size: int,
                 text: str,
                 font_color: Tuple[int, int, int],
                 font_hoover_color: Tuple[int, int, int],
                 font_clicked_color: Tuple[int, int, int],
                 callbacks=None):
        super().__init__(x, y, font, font_size, font_color, text)

        if callbacks is None:
            callbacks = []
        self.is_clicked_ = False
        self.is_clickable_ = True
        self.callbacks_ = callbacks
        self.image_ = pygame.rect.Rect(self.point_.x, self.point_.y, self.text_.get_width(), self.text_.get_height())

        if isinstance(font_hoover_color, tuple) and isinstance(font_clicked_color, tuple):
            self.base_color_ = self.font_color_
            self.hoover_color_ = font_hoover_color
            self.clicked_color_ = font_clicked_color
        else:
            raise TypeError("buttons hoover and click colors has to be a tuple of 3 integers (RGB)")

        if not self.callbacks_:
            self.callbacks_ = []
        else:
            if isinstance(callbacks, list):
                self.callbacks_ = callbacks
            else:
                raise TypeError("callbacks has to be a list of functions (callables)")

        self.after_click_delayer_ = -1

    def set_click(self, clicked: bool) -> None:
        if self.is_clicked_ is not clicked:
            self.is_clicked_ = clicked
            if self.is_clicked_:
                self.after_click_delayer_ += 1
            else:
                if not (self.after_click_delayer_ == -1):
                    self.after_click_delayer_ = -1

    @property
    def is_clicked(self):
        return self.is_clicked_

    @is_clicked.setter
    def is_clicked(self, clicked: bool = True):
        self.set_click(clicked)

    def toggle_click(self):
        self.set_click(not self.is_clicked_)

    def set_clickability(self, clickability: bool) -> None:
        if self.is_clickable_ is not clickability:
            self.is_clickable_ = clickability
            self.color()

    @property
    def is_clickable(self):
        return self.is_clickable_

    @is_clickable.setter
    def is_clickable(self, clickability: bool = True) -> None:
        self.set_clickability(clickability)

    def toggle_clickability(self):
        self.set_clickability(not self.is_clickable_)

    def check_for_click(self, position: Tuple[int, int], clicked: bool) -> bool:
        if not self.is_hidden_ and self.is_clickable_:
            if self.image_.collidepoint(position) and clicked:
                self.toggle_click()
                self.color()
                self.call()
                return True
        return False

    def check_for_hoover(self, position: Tuple[int, int]) -> bool:
        if not self.is_hidden_ and self.is_clickable_:
            if self.image_.collidepoint(position):
                self.font_color = self.hoover_color_
                return True
            else:
                self.color()
        return False

    def call(self):
        print(f"callbacks: {self.callbacks_}")
        for func, args in self.callbacks_:
            if args is None:
                func()
            else:
                func(args)

    def color(self):
        if self.is_clicked_ and self.is_clickable_:
            self.font_color_ = self.clicked_color_
        else:
            self.font_color_ = self.base_color_

    def after_click_delay(self) -> bool:
        # deprecated
        if self.after_click_delayer_ == -1:
            return True
        elif 0 <= self.after_click_delayer_ <= Button.AFTER_CLICK_DELAYER:
            self.after_click_delayer_ += 1
            self.set_clickability(False)
            return False
        elif self.after_click_delayer_ > Button.AFTER_CLICK_DELAYER:
            self.after_click_delayer_ = -1
            self.set_clickability(True)
            return True
        else:
            raise RuntimeError("There is no procedure for this button delayer case")

    def set_callback(self, func: Callable, args: None | int | float | str = None) -> None:
        self.callbacks_ = [[func, args]]

    def add_callback(self, func: Callable, args: None | int | float | str = None) -> None:
        if not self.callbacks_:
            self.callbacks_ = []
        self.callbacks_.append([func, args])

    def get_callbacks(self) -> list:
        return self.callbacks_

    def render(self, display: pygame.Surface):
        mouse_position = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        self.check_for_click(mouse_position, mouse_click)
        self.check_for_hoover(mouse_position)

        if self.is_hidden_:
            self.text_ = self.font_.render("", True, self.font_color_)
            self.is_clickable = False
            self.is_clicked = False
        else:
            self.font_ = pygame.font.Font(self.font_path_, self.font_size_)
            self.text_ = self.font_.render(self.raw_text_, True, self.font_color_)
            self.image_ = pygame.rect.Rect(self.point_.x - self.text_.get_width() / 2,
                                           self.point_.y - self.text_.get_height() / 2,
                                           self.text_.get_width(),
                                           self.text_.get_height())
            display.blit(self.text_, (self.point_.x - self.image_.width / 2, self.point_.y - self.image_.height / 2))


class PushButton(Button):
    """
    PushButtons are simply buttons that keep their state (pressed or not).
    They do not use hoover color but a "pressed" and "released" state.
    """

    def __init__(self, x: int | float, y: int | float,
                 font: str,
                 font_size: int,
                 text: str,
                 font_color: Tuple[int, int, int],
                 font_hoover_color: Tuple[int, int, int],
                 callbacks=None) -> None:
        super().__init__(x, y,
                         font,
                         font_size,
                         text,
                         font_color,
                         font_hoover_color,
                         font_color,
                         callbacks=callbacks)

    def check_for_click(self, position: Tuple[int, int], clicked: bool) -> bool:
        if not self.is_hidden_ and self.is_clickable_:
            if self.image_.collidepoint(position) and clicked:
                self.color()
                self.call()
                return True
        return False


class CheckBox(Button):
    def __init__(self,
                 x: int, y: int,
                 size: int,
                 checked: bool,
                 base_color: Tuple[int, int, int],
                 hoover_color: Tuple[int, int, int],
                 clicked_color: Tuple[int, int, int],
                 line_width: int = 2,
                 callbacks=None) -> None:
        if isinstance(checked, bool):
            self.is_clicked_ = checked
        if isinstance(line_width, int) and line_width > 0:
            self.line_width_ = line_width
        else:
            raise ValueError("Line width should be an integer strictly greater than 0")
        super().__init__(x, y,
                         Fonts.COMIC_SANS_MS,
                         size,
                         "",
                         base_color,
                         hoover_color,
                         clicked_color,
                         callbacks=callbacks)
        self.rectangle_ = pygame.rect.Rect(self.point_.x, self.point_.y, self.font_size_, self.font_size_)

    def draw_checked(self, display: pygame.Surface):
        self.draw_unchecked(display)
        pygame.draw.line(display, self.font_color_, (self.point_.x, self.point_.y),
                         (self.point_.x + self.font_size_, self.point_.y + self.font_size_))
        pygame.draw.line(display, self.font_color_, (self.point_.x, self.point_.y + self.font_size_),
                         (self.point_.x + self.font_size_, self.point_.y))

    def draw_unchecked(self, display: pygame.Surface):
        pygame.draw.line(display, self.font_color_, (self.point_.x, self.point_.y),
                         (self.point_.x + self.font_size_, self.point_.y))
        pygame.draw.line(display, self.font_color_, (self.point_.x, self.point_.y),
                         (self.point_.x, self.point_.y + self.font_size_))
        pygame.draw.line(display, self.font_color_, (self.point_.x + self.font_size_, self.point_.y + self.font_size_),
                         (self.point_.x + self.font_size_, self.point_.y))
        pygame.draw.line(display, self.font_color_, (self.point_.x + self.font_size_, self.point_.y + self.font_size_),
                         (self.point_.x, self.point_.y + self.font_size_))

    def render(self, display: pygame.Surface) -> None:
        mouse_position = pygame.mouse.get_pos()
        right_mouse_click = pygame.mouse.get_pressed()[0]
        self.check_for_click(mouse_position, right_mouse_click)
        self.check_for_hoover(mouse_position)
        if not self.is_hidden_:
            if self.is_clicked_ and self.is_clickable_:
                self.draw_checked(display)
            else:
                self.draw_unchecked(display)
            # self.rectangle_ = pygame.rect.Rect(self.point_.x, self.point_.y, self.size_, self.size_)

    def check_for_hoover(self, position: Tuple[int, int]):
        if not self.is_hidden_ and self.is_clickable_:
            if self.rectangle_.collidepoint(position):
                self.font_color_ = self.hoover_color_
            else:
                self.color()

    def check_for_click(self, position: Tuple[int, int], clicked: bool):
        if self.is_clickable_ and not self.is_hidden_:
            if self.rectangle_.collidepoint(position) and clicked:
                self.toggle_click()
                self.color()
                self.call()


class ClickableImage(PushButton):
    pass


def print_test(text: str = "Clicked !") -> None:
    print(text)


def test_button():
    pygame.init()
    display = pygame.display.set_mode((600, 600))

    buttons: list = [
        Button(int(Settings.WINDOW_SIZE * .5),
               int(Settings.WINDOW_SIZE * .35),
               Fonts.HERCULANUM,
               50,
               "Button",
               Colors.WHITE,
               Colors.GREEN,
               Colors.RED,
               [[print_test, "Button"]]),
        PushButton(int(Settings.WINDOW_SIZE * .5),
                   int(Settings.WINDOW_SIZE * .5),
                   Fonts.HERCULANUM,
                   70,
                   "PushButton",
                   Colors.RED,
                   Colors.GREEN,
                   [[print_test, "PushButton"]]),
        Button(int(Settings.WINDOW_SIZE * .5),
               int(Settings.WINDOW_SIZE * .75),
               Fonts.HERCULANUM,
               50,
               "Button_2",
               Colors.WHITE,
               Colors.GREEN,
               Colors.RED,
               [[print_test, "Button1"]]),
        CheckBox(20, 20, 50, True, Colors.WHITE, Colors.RED, Colors.RED, line_width=8,
                 callbacks=[[print_test, "CheckBox"]])
    ]
    counter = 0
    while counter < 1000:

        for event in pygame.event.get() + [pygame.event.wait()]:
            if event.type == pygame.QUIT:
                break

        # testing the main methods of the Label class
        if counter > 200:
            buttons[0].text = str(counter)
            # buttons[0].font_size += 1
        if counter > 100:
            buttons[0].is_clickable = False
        if counter > 300:
            buttons[0].is_hidden = True
        if counter > 350:
            pass
            # buttons[1].is_hidden = True

        # rendering the label
        for button in buttons:
            button.render(display)

        counter += 1
        pygame.display.update()
        display.fill(Colors.BLACK)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    test_button()
