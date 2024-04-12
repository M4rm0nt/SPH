import random

import pygame

from src.utilities.einstellungen import bild_laden, BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE


class Erzquelle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('erz')
        self.rect = self.image.get_rect(center=(random.randint(100, BILDSCHIRM_BREITE - 100), random.randint(50, BILDSCHIRM_HOEHE - 50)))
        self.erz_menge = 1000

    def neupositionieren(self):
        self.rect.center = (random.randint(100, BILDSCHIRM_BREITE - 100), random.randint(50, BILDSCHIRM_HOEHE - 50))