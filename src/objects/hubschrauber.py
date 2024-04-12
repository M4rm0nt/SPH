import pygame
from src.utilities.einstellungen import bild_laden


class Hubschrauber(pygame.sprite.Sprite):
    def __init__(self, lkw, hubschrauberlandeplatz, geschwindigkeit):
        super().__init__()
        self.original_image = bild_laden('hubschrauber')
        self.image = self.original_image
        self.rect = self.image.get_rect(center=hubschrauberlandeplatz.rect.center)
        self.rect.inflate_ip(-self.rect.width * 0.5, -self.rect.height * 0.5)
        self.geschwindigkeit = geschwindigkeit
        self.lkw = lkw
        self.hubschrauberlandeplatz = hubschrauberlandeplatz
        self.reset_required = False
        self.ausrichtung = "rechts"

    def update(self):
        if self.reset_required:
            self.zuruecksetzen_zu_hubschrauberlandeplatz()
        else:
            self.lkw_verfolgen()

    def lkw_verfolgen(self):
        if self.lkw.rect.centerx < self.rect.centerx:
            self.rect.x -= self.geschwindigkeit
            neue_ausrichtung = "links"
        elif self.lkw.rect.centerx > self.rect.centerx:
            self.rect.x += self.geschwindigkeit
            neue_ausrichtung = "rechts"
        else:
            neue_ausrichtung = self.ausrichtung

        if neue_ausrichtung != self.ausrichtung:
            self.ausrichtung = neue_ausrichtung
            self.spiegeln()

        if self.lkw.rect.centery < self.rect.centery:
            self.rect.y -= self.geschwindigkeit
        elif self.lkw.rect.centery > self.rect.centery:
            self.rect.y += self.geschwindigkeit

    def spiegeln(self):
        if self.ausrichtung == "rechts":
            self.image = pygame.transform.flip(self.original_image, False, False)
        elif self.ausrichtung == "links":
            self.image = pygame.transform.flip(self.original_image, True, False)
        self.rect = self.image.get_rect(center=self.rect.center)

    def zuruecksetzen_zu_hubschrauberlandeplatz(self):
        self.rect.center = self.hubschrauberlandeplatz.rect.center
        self.reset_required = False
