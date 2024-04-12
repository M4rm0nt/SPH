import pygame

from src.game.einstellungen import bild_laden


class Hubschrauber(pygame.sprite.Sprite):
    def __init__(self, lkw, hubschrauberlandeplatz, geschwindigkeit):
        super().__init__()
        self.image = bild_laden('hubschrauber')
        self.rect = self.image.get_rect(center=hubschrauberlandeplatz.rect.center)
        self.rect.inflate_ip(-self.rect.width * 0.5, -self.rect.height * 0.5)
        self.geschwindigkeit = geschwindigkeit
        self.lkw = lkw
        self.hubschrauberlandeplatz = hubschrauberlandeplatz
        self.reset_required = False

    def update(self):
        if self.reset_required:
            self.zuruecksetzen_zu_hubschrauberlandeplatz()
        else:
            self.lkw_verfolgen()

    def lkw_verfolgen(self):
        if self.lkw.rect.centerx < self.rect.centerx:
            self.rect.x -= self.geschwindigkeit
        elif self.lkw.rect.centerx > self.rect.centerx:
            self.rect.x += self.geschwindigkeit
        if self.lkw.rect.centery < self.rect.centery:
            self.rect.y -= self.geschwindigkeit
        elif self.lkw.rect.centery > self.rect.centery:
            self.rect.y += self.geschwindigkeit

    def zuruecksetzen_zu_hubschrauberlandeplatz(self):
        self.rect.center = self.hubschrauberlandeplatz.rect.center
        self.reset_required = False
