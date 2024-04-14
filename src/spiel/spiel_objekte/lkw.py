from math import sqrt

import pygame
from main import bild_laden


class LKW(pygame.sprite.Sprite):
    def __init__(self, geschwindigkeit):
        super().__init__()
        self.original_bild = bild_laden('lastwagen')
        self.image = self.original_bild
        self.rect = self.original_bild.get_rect(center=(400, 550))
        self.hitbox = pygame.Rect(self.rect.left + 40, self.rect.top + 40, self.rect.width - 80, self.rect.height - 80)
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
        lkw_x = 0
        lkw_y = 0
        richtung_geaendert = False

        if tasten[pygame.K_LEFT]:
            lkw_x -= self.geschwindigkeit
            if self.ausrichtung != "links":
                self.ausrichtung = "links"
                richtung_geaendert = True
        if tasten[pygame.K_RIGHT]:
            lkw_x += self.geschwindigkeit
            if self.ausrichtung != "rechts":
                self.ausrichtung = "rechts"
                richtung_geaendert = True
        if tasten[pygame.K_UP]:
            lkw_y -= self.geschwindigkeit
        if tasten[pygame.K_DOWN]:
            lkw_y += self.geschwindigkeit

        if lkw_x != 0 and lkw_y != 0:
            norm = sqrt(2)
            lkw_x /= norm
            lkw_y /= norm

        self.rect.x += int(lkw_x)
        self.rect.y += int(lkw_y)

        self.rect.x = max(0, min(800 - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(600 - self.rect.height, self.rect.y))
        self.hitbox.center = self.rect.center

        if richtung_geaendert:
            self.spiegeln()

    def spiegeln(self):
        if self.ausrichtung == "rechts":
            self.image = pygame.transform.flip(self.original_bild, False, False)
        elif self.ausrichtung == "links":
            self.image = pygame.transform.flip(self.original_bild, True, False)
        self.rect = self.image.get_rect(center=self.rect.center)

    def kraftstoff_verbrauchen(self, tasten):
        if any(tasten[key] for key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)):
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
