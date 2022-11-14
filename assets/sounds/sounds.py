# -*- coding:utf-8 -*-
__projet__ = "Chess"
__nom_fichier__ = "sounds"
__author__ = "PENOT Baptiste"
__date__ = "août 2022"

import os
import pygame
from pygame.mixer import Sound
from settings import (
    Directories
)


class SoundEffects:
    """
    Class responsible for sounds while moving pieces on the chess board.
    """
    pygame.mixer.init()
    SELECT_SOUND: Sound = pygame.mixer.Sound(os.path.join(Directories.ASSETS_DIR, "sounds/selection_sound.mp3"))
    EAT_SOUND: Sound = pygame.mixer.Sound(os.path.join(Directories.ASSETS_DIR, "sounds/eat_sound.mp3"))
    SLIDE_SOUND: Sound = pygame.mixer.Sound(os.path.join(Directories.ASSETS_DIR, "sounds/slide_sound.mp3"))


def play_sound(select_sound: bool = False, eat_sound: bool = False, slide_sound: bool = False) -> bool:
    """
    Play a sound depending on the input and return True if a sound was played.
    Otherwise, return False.
    If no arguments, do not play any sound.
    :param select_sound: if true play the selection sound (when you pick a piece)
    :param eat_sound:  if true play the eating sound (when you eat another piece)
    :param slide_sound: if true play the sliding sound (when you slide a piece)
    """
    if select_sound:
        SoundEffects.SELECT_SOUND.play()
        return True
    elif eat_sound:
        SoundEffects.EAT_SOUND.play()
        return True
    elif slide_sound:
        SoundEffects.SLIDE_SOUND.play()
        return True
    return False
