import random

import pygame

from main import bild_laden


class Hubschrauberlandeplatz(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('hubschrauberlandeplatz')
        self.rect = self.image.get_rect(center=(random.randint(50, 650), random.randint(50, 550)))