import random

import pygame

from main import bild_laden


class Hubschrauberlandeplatz(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('hubschrauberlandeplatz')
        self.rect = self.image.get_rect(center=(random.randint(340, 460), random.randint(100, 500)))
