import random

import pygame
from main import bild_laden


class Erzquelle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('erz')
        self.rect = self.image.get_rect(center=(random.randint(100, 700), random.randint(100, 500)))
        self.erz_menge = 1000

    def neupositionieren(self):
        self.rect.center = (random.randint(100, 700), random.randint(100, 500))
