import pygame
from main import bild_laden


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
        else:
            self.bewegen_zu(self.hubschrauberlandeplatz.rect.centerx, self.hubschrauberlandeplatz.rect.centery)

    def erz_abladen(self):
        self.abgeladenes_erz += self.gestohlenes_erz
        self.gestohlenes_erz = 0
        self.erz_gestohlen = False

    def bewegen_zu(self, lkw_x, lkw_y):
        hubschrauber_x = lkw_x - self.rect.centerx
        hubschrauber_y = lkw_y - self.rect.centery
        distanz = (hubschrauber_x ** 2 + hubschrauber_y ** 2) ** 0.5

        if distanz < self.geschwindigkeit or distanz == 0:
            self.rect.center = (lkw_x, lkw_y)
        else:
            schritt_x = hubschrauber_x / distanz * self.geschwindigkeit
            schritt_y = hubschrauber_y / distanz * self.geschwindigkeit
            self.rect.x += int(schritt_x)
            self.rect.y += int(schritt_y)

        if hubschrauber_x > 0 and abs(hubschrauber_x) > abs(hubschrauber_y):
            neue_ausrichtung = "rechts"
        elif hubschrauber_x < 0 and abs(hubschrauber_x) > abs(hubschrauber_y):
            neue_ausrichtung = "links"
        else:
            neue_ausrichtung = self.ausrichtung

        if neue_ausrichtung != self.ausrichtung:
            self.ausrichtung = neue_ausrichtung
            self.spiegeln()

    def spiegeln(self):
        if self.ausrichtung == "rechts":
            self.image = pygame.transform.flip(self.original_image, False, False)
        elif self.ausrichtung == "links":
            self.image = pygame.transform.flip(self.original_image, True, False)
        self.rect = self.image.get_rect(center=self.rect.center)
