import pygame
from src.utilities.einstellungen import bild_laden


class Hubschrauber(pygame.sprite.Sprite):
    def __init__(self, lkw, hubschrauberlandeplatz, geschwindigkeit):
        super().__init__()
        self.original_image = bild_laden('hubschrauber')
        self.image = self.original_image
        self.rect = self.image.get_rect(center=hubschrauberlandeplatz.rect.center)
        self.geschwindigkeit = geschwindigkeit
        self.lkw = lkw
        self.hubschrauberlandeplatz = hubschrauberlandeplatz
        self.erz_gestohlen = False
        self.gestohlenes_erz = 0
        self.abgeladenes_erz = 0
        self.ausrichtung = "rechts"

    def update(self):
        if self.erz_gestohlen:
            self.zum_hubschrauberlandeplatz_fliegen()
        else:
            self.lkw_verfolgen()

    def lkw_verfolgen(self):
        if self.rect.colliderect(self.lkw.rect) and self.lkw.erz_geladen():
            self.gestohlenes_erz += self.lkw.erz
            self.lkw.erz = 0
            self.erz_gestohlen = True

        self.bewegen_zu(self.lkw.rect.centerx, self.lkw.rect.centery)

    def zum_hubschrauberlandeplatz_fliegen(self):
        if self.rect.center == self.hubschrauberlandeplatz.rect.center:
            self.erz_abladen()
            return
        self.bewegen_zu(self.hubschrauberlandeplatz.rect.centerx, self.hubschrauberlandeplatz.rect.centery)

    def erz_abladen(self):
        self.abgeladenes_erz += self.gestohlenes_erz
        self.gestohlenes_erz = 0
        self.erz_gestohlen = False

    def bewegen_zu(self, hubschrauberlandeplatz_mitte_x, hubschrauberlandeplatz_mitte_y):
        ziel_x = hubschrauberlandeplatz_mitte_x - self.rect.centerx
        ziel_y = hubschrauberlandeplatz_mitte_y - self.rect.centery
        if ziel_x != 0:
            self.rect.x += self.geschwindigkeit if ziel_x > 0 else -self.geschwindigkeit
        if ziel_y != 0:
            self.rect.y += self.geschwindigkeit if ziel_y > 0 else -self.geschwindigkeit

        neue_ausrichtung = "rechts" if ziel_x > 0 else "links"
        if neue_ausrichtung != self.ausrichtung:
            self.ausrichtung = neue_ausrichtung
            self.spiegeln()

    def spiegeln(self):
        if self.ausrichtung == "rechts":
            self.image = pygame.transform.flip(self.original_image, False, False)
        elif self.ausrichtung == "links":
            self.image = pygame.transform.flip(self.original_image, True, False)
        self.rect = self.image.get_rect(center=self.rect.center)
