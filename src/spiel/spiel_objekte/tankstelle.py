import random

import pygame

from main import bild_laden


class Tankstelle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('tankstelle')
        self.rect = self.image.get_rect(center=(random.randint(50, 750), random.randint(50, 550)))
