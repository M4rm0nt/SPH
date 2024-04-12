import pygame
from src.utilities.einstellungen import bild_laden, BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE, Tasten

class LKW(pygame.sprite.Sprite):
    def __init__(self, geschwindigkeit):
        super().__init__()
        self.lkw_image = bild_laden('lastwagen')
        self.image = self.lkw_image
        self.rect = self.lkw_image.get_rect(center=(BILDSCHIRM_BREITE // 2, BILDSCHIRM_HOEHE - 50))
        self.hitbox = pygame.Rect(self.rect.left + 10, self.rect.top + 10, self.rect.width - 20, self.rect.height - 20)
        self.geschwindigkeit = geschwindigkeit
        self.kraftstoff = 100
        self.erz = 0
        self.max_erz = 50
        self.ausrichtung = "rechts"

    def update(self, tasten, erz_quelle, lager, tankstelle, hubschrauber_gruppe):
        self.bewegen(tasten)
        self.kraftstoff_verbrauchen(tasten)
        self.kollision_pruefen(erz_quelle, lager, tankstelle, hubschrauber_gruppe)

    def bewegen(self, tasten):
        richtung_geaendert = False
        if tasten[Tasten.LINKS.value] or tasten[Tasten.A.value]:
            self.rect.x -= self.geschwindigkeit
            if self.ausrichtung != "links":
                self.ausrichtung = "links"
                richtung_geaendert = True
        if tasten[Tasten.RECHTS.value] or tasten[Tasten.D.value]:
            self.rect.x += self.geschwindigkeit
            if self.ausrichtung != "rechts":
                self.ausrichtung = "rechts"
                richtung_geaendert = True
        if tasten[Tasten.OBEN.value] or tasten[Tasten.W.value]:
            self.rect.y -= self.geschwindigkeit
        if tasten[Tasten.UNTEN.value] or tasten[Tasten.S.value]:
            self.rect.y += self.geschwindigkeit

        if richtung_geaendert:
            self.drehen()

        self.rect.x = max(0, min(BILDSCHIRM_BREITE - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(BILDSCHIRM_HOEHE - self.rect.height, self.rect.y))
        self.hitbox.center = self.rect.center

    def drehen(self):
        if self.ausrichtung == "rechts":
            self.image = pygame.transform.flip(self.lkw_image, False, False)
        elif self.ausrichtung == "links":
            self.image = pygame.transform.flip(self.lkw_image, True, False)
        self.rect = self.image.get_rect(center=self.rect.center)

    def kraftstoff_verbrauchen(self, tasten):
        if any(tasten[key.value] for key in [Tasten.LINKS, Tasten.RECHTS, Tasten.OBEN, Tasten.UNTEN, Tasten.W, Tasten.A, Tasten.S, Tasten.D]):
            self.kraftstoff -= 0.15
            if self.kraftstoff <= 0:
                self.kill()

    def kollision_pruefen(self, erz_quelle, lager, tankstelle, hubschrauber_gruppe):
        kollidierter_hubschrauber = pygame.sprite.spritecollideany(self, hubschrauber_gruppe, collided=lambda s1, s2: s1.hitbox.colliderect(s2.rect))
        if kollidierter_hubschrauber and self.erz > 0:
            self.erz = 0
            kollidierter_hubschrauber.erz_gestohlen = True
        if self.hitbox.colliderect(erz_quelle.rect):
            self.erz_sammeln(erz_quelle)
        if self.hitbox.colliderect(lager.rect):
            lager.erz += self.erz
            self.erz = 0
        if self.hitbox.colliderect(tankstelle.rect):
            self.kraftstoff = 100

    def erz_sammeln(self, erz_quelle):
        if self.erz < self.max_erz and erz_quelle.erz_menge > 0:
            zu_bergendes_erz = min(self.max_erz - self.erz, erz_quelle.erz_menge)
            self.erz += zu_bergendes_erz
            erz_quelle.erz_menge -= zu_bergendes_erz
            if self.erz == self.max_erz:
                erz_quelle.neupositionieren()

    def erz_geladen(self):
        return self.erz > 0
