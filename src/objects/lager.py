import pygame

from src.game.einstellungen import bild_laden, BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE


class Lager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('lager')
        self.rect = self.image.get_rect(center=(BILDSCHIRM_BREITE - 150, BILDSCHIRM_HOEHE // 2))
        self.erz = 0
        self.kapazitaet = 1000
