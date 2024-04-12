import random

import pygame

from src.game.einstellungen import bild_laden, BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE


class Tankstelle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('tankstelle')
        self.rect = self.image.get_rect(center=(random.randint(50, BILDSCHIRM_BREITE - 50), random.randint(50, BILDSCHIRM_HOEHE - 50)))
