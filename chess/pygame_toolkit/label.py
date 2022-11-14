import pygame
from typing import Tuple
import os
from settings import Colors, Fonts, Directories
from chess.pygame_toolkit.point import Point


class Label:
    def __init__(self,
                 x: int | float, y: int | float,
                 font: str, font_size: int, font_color: Tuple[int, int, int],
                 text: str):
        self.point_ = Point(x, y)
        pygame.font.init()
        self.font_color = font_color
        # about fonts
        if isinstance(font, str) and isinstance(font_size, int):
            if font_size > 0:
                if os.path.exists(font):
                    self.font_path_ = font
                else:
                    raise FileNotFoundError("Path to font does not exists")
                self.font_ = pygame.font.Font(font, font_size)
                self.font_size_ = font_size
            else:
                raise ValueError("The font should be a integer greater than zero")
        else:
            raise TypeError("Font should be the path to the font file and font_size a strictly positive integer")

        # about text
        if isinstance(text, str) and isinstance(font_color, tuple):
            # True in second position is for anti-aliasing
            self.text_ = self.font_.render(text, True, font_color)
            self.raw_text_ = text
            self.font_color_ = font_color
        else:
            raise TypeError(
                "The text has to be a string and the font color a tuple of 3 integers between 0 and 255 (RGB)")
        self.is_hidden_ = False

    def set_x(self, new_x: int | float) -> None:
        if isinstance(new_x, int):
            self.point_.x = new_x
        else:
            raise TypeError("attribute x of Point object has to be an  integer")

    @property
    def x(self) -> int | float:
        return self.point_.x

    @x.setter
    def x(self, new_x: int | float) -> None:
        self.set_x(new_x)

    def set_y(self, new_y: int | float) -> None:
        if isinstance(new_y, int):
            self.point_.y = new_y
        else:
            raise TypeError("attribute y of Point object has to be an  integer")

    @property
    def y(self) -> int | float:
        return self.point_.y

    @y.setter
    def y(self, new_y: int | float) -> None:
        self.set_y(new_y)

    def set_text(self, new_text: str) -> None:
        if isinstance(new_text, str):
            self.raw_text_ = new_text
        else:
            raise TypeError("The text should be a string")

    @property
    def text(self) -> str:
        return self.raw_text_

    @text.setter
    def text(self, new_text: str) -> None:
        self.set_text(new_text)

    def set_font_size(self, new_font_size: int) -> None:
        if isinstance(new_font_size, int):
            self.font_size_ = new_font_size
        else:
            raise TypeError("The font size should be an integer")

    @property
    def font_size(self) -> int:
        return self.font_size_

    @font_size.setter
    def font_size(self, new_font_size: int) -> None:
        self.set_font_size(new_font_size)

    def set_font(self, new_font_path: str) -> None:
        if isinstance(new_font_path, str):
            if os.path.exists(new_font_path):
                self.font_path_ = new_font_path
            else:
                raise FileNotFoundError("The requested font path does not exists")
        else:
            raise TypeError("The font should be a valid path, as a string")

    @property
    def font(self) -> str:
        return self.font_path_

    @font.setter
    def font(self, new_font_path: str) -> None:
        self.set_font(new_font_path)

    def set_font_color(self, new_rgb_font_color: Tuple[int, int, int]) -> None:
        if isinstance(new_rgb_font_color, tuple):
            self.font_color_ = new_rgb_font_color
        else:
            raise TypeError("The font color should be a tuple of three integers (RGB)")

    @property
    def font_color(self) -> Tuple[int, int, int]:
        return self.font_color_

    @font_color.setter
    def font_color(self, new_rgb_font_color: Tuple[int, int, int]) -> None:
        self.set_font_color(new_rgb_font_color)

    def set_is_hidden(self, is_hidden: bool) -> None:
        if isinstance(is_hidden, bool):
            if is_hidden is not self.is_hidden_:
                self.is_hidden_ = is_hidden

    @property
    def is_hidden(self) -> bool:
        return self.is_hidden_

    @is_hidden.setter
    def is_hidden(self, is_hidden: bool) -> None:
        self.set_is_hidden(is_hidden)

    def toggle_visibility(self):
        self.is_hidden_ = not self.is_hidden_

    def render(self, display: pygame.Surface):
        self.font_ = pygame.font.Font(self.font_path_, self.font_size_)
        if self.is_hidden_:
            # todo why not to just write pass here ?
            self.text_ = self.font_.render("", True, self.font_color_)
        else:
            self.text_ = self.font_.render(self.raw_text_, True, self.font_color_)
        display.blit(self.text_,
                     (self.point_.x - self.text_.get_width() / 2, self.point_.y - self.text_.get_height() / 2))


class Image(Label):
    """
    This Image class implement is a high-level code implementing images for pygame
    """

    def __init__(self,
                 x: int | float, y: int | float,
                 scale: int | float,
                 image: str,
                 convert_alpha: bool = False
                 ) -> None:
        super().__init__(x, y, Fonts.COMIC_SANS_MS, 1, Colors.BLACK, "")
        pygame.display.init()

        if isinstance(convert_alpha, bool):
            self.convert_alpha_ = convert_alpha
        else:
            raise TypeError("Wrong type for convert alpha argument during Image(Label) class construction")
        if isinstance(scale, float) and scale > 0:
            self.scale_ = scale
        else:
            raise ValueError("scale should be a float strictly superior to zero")
        if os.path.exists(image):
            self.image_path_ = image
            self.image_ = None
            self.load()
        else:
            raise FileNotFoundError("images for the button not found")

    def set_scale(self, new_scale: int | float) -> None:
        if isinstance(new_scale, float) and new_scale > 0:
            self.scale_ = new_scale
            self.load()
        else:
            raise TypeError("image scale has to be strictly positive and float typed")

    @property
    def scale(self):
        return self.scale_

    @scale.setter
    def scale(self, new_scale: int | float):
        self.set_scale(new_scale)

    def set_image_path(self, new_image_path: str) -> None:
        if os.path.exists(new_image_path):
            self.image_path_ = new_image_path
            self.load()
        else:
            raise TypeError("images for the button not found")

    @property
    def image_path(self):
        return self.image_path_

    @image_path.setter
    def image_path(self, new_image_path: str):
        self.set_image_path(new_image_path)

    def set_convert_alpha(self, value: bool) -> None:
        if isinstance(value, bool):
            if value is not self.convert_alpha_:
                self.convert_alpha_ = value
        else:
            raise TypeError("Wrong type for convert alpha argument during Image(Label) class construction")

    @property
    def convert_alpha(self) -> bool:
        return self.convert_alpha_

    @convert_alpha.setter
    def convert_alpha(self, alpha: bool) -> None:
        self.set_convert_alpha(alpha)

    def load(self):
        if self.convert_alpha_:
            self.image_ = pygame.image.load(self.image_path_).convert_alpha()
        else:
            self.image_ = pygame.image.load(self.image_path_)
        self.image_ = pygame.transform.scale(self.image_,
                                             (int(self.image_.get_width() * self.scale_),
                                              int(self.image_.get_height() * self.scale_)))

    def render(self, display: pygame.Surface):
        if not self.is_hidden_:
            display.blit(self.image_, (self.point_.x, self.point_.y))


def test():
    pygame.init()
    display = pygame.display.set_mode((600, 600))
    labels: list = [
        Label(300, 300, Fonts.HERCULANUM, 40, Colors.RED, ""),
        Label(100, 50, Fonts.HERCULANUM, 70, Colors.GREEN, "TEST ;)"),
        Label(300, 500, Fonts.COMIC_SANS_MS, 5, Colors.WHITE, "Yooo"),
        Image(10, 400, .3, os.path.join(Directories.ASSETS_DIR, "game_icon/game_icon.png"))
    ]
    run = True
    counter = 0
    while run:

        events = pygame.event.get() + [pygame.event.wait()]
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        # testing the main methods of the Label class
        # text setter
        labels[0].text = str(counter)
        # font color setter
        if counter > 50:
            labels[1].font_color = Colors.PURPLE
        # font size setter
        labels[2].font_size += 1
        # font setter
        if counter > 50:
            labels[0].font = Fonts.COMIC_SANS_MS_BOLD
        if counter > 60:
            labels[1].is_hidden = True
        if counter > 400:
            labels[2].is_hidden_ = True
            labels[3].is_hidden_ = True
        if counter > 500:
            labels[3].is_hidden_ = False
        if counter > 550:
            labels[3].image_path = os.path.join(Directories.ASSETS_DIR, "screenshots/main_menu.png")

        # rendering the label
        for label in labels:
            label.render(display)

        counter += 1
        pygame.display.update()
        display.fill(Colors.BLACK)
    pygame.quit()
    exit()


if __name__ == '__main__':
    test()
