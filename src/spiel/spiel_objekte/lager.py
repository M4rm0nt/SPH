import random

import pygame

from main import bild_laden


class Lager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('lager')
        self.rect = self.image.get_rect(center=(random.randint(460, 580), random.randint(100, 500)))
        self.erz = 0
        self.kapazitaet = 1000
