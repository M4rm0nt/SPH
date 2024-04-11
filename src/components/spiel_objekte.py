import pygame
import random

from src.einstellungen import bild_laden, BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE, Tasten


class LKW(pygame.sprite.Sprite):
    def __init__(self, geschwindigkeit):
        super().__init__()
        self.image = bild_laden('lastwagen')
        self.rect = self.image.get_rect(center=(BILDSCHIRM_BREITE // 2, BILDSCHIRM_HOEHE - 50))
        self.hitbox = pygame.Rect(self.rect.left + 10, self.rect.top + 10, self.rect.width - 20, self.rect.height - 20)
        self.geschwindigkeit = geschwindigkeit
        self.kraftstoff = 100
        self.erz = 0
        self.max_erz = 50
        self.gestohlenes_erz = 0

    def update(self, tasten, erz_quelle, lager, tankstelle, hubschrauber_gruppe):
        self.bewegen(tasten)
        self.kraftstoff_verbrauchen(tasten)
        self.kollision_pruefen(erz_quelle, lager, tankstelle, hubschrauber_gruppe)

    def bewegen(self, tasten):
        if tasten[Tasten.LINKS.value] or tasten[Tasten.A.value]:
            self.rect.x -= self.geschwindigkeit
        if tasten[Tasten.RECHTS.value] or tasten[Tasten.D.value]:
            self.rect.x += self.geschwindigkeit
        if tasten[Tasten.OBEN.value] or tasten[Tasten.W.value]:
            self.rect.y -= self.geschwindigkeit
        if tasten[Tasten.UNTEN.value] or tasten[Tasten.S.value]:
            self.rect.y += self.geschwindigkeit
        self.rect.x = max(0, min(BILDSCHIRM_BREITE - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(BILDSCHIRM_HOEHE - self.rect.height, self.rect.y))
        self.hitbox.center = self.rect.center

    def kraftstoff_verbrauchen(self, tasten):
        if any(tasten[key.value] for key in [Tasten.LINKS, Tasten.RECHTS, Tasten.OBEN, Tasten.UNTEN, Tasten.W, Tasten.A, Tasten.S, Tasten.D]):
            self.kraftstoff -= 0.15
            if self.kraftstoff <= 0:
                self.kill()

    def kollision_pruefen(self, erz_quelle, lager, tankstelle, hubschrauber_gruppe):
        kollidierter_hubschrauber = pygame.sprite.spritecollideany(self, hubschrauber_gruppe,
                                                                   collided=lambda s1, s2: s1.hitbox.colliderect(s2.rect))
        if kollidierter_hubschrauber and self.erz > 0:
            self.gestohlenes_erz += self.erz
            self.erz = 0
            kollidierter_hubschrauber.reset_required = True
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


class Hubschrauberlandeplatz(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('hubschrauberlandeplatz')
        self.rect = self.image.get_rect(center=(random.randint(50, BILDSCHIRM_BREITE - 150), random.randint(50, BILDSCHIRM_HOEHE - 50)))


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



class Erzquelle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('erz')
        self.rect = self.image.get_rect(center=(random.randint(100, BILDSCHIRM_BREITE - 100), random.randint(50, BILDSCHIRM_HOEHE - 50)))
        self.erz_menge = 1000

    def neupositionieren(self):
        self.rect.center = (random.randint(100, BILDSCHIRM_BREITE - 100), random.randint(50, BILDSCHIRM_HOEHE - 50))


class Lager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('lager')
        self.rect = self.image.get_rect(center=(BILDSCHIRM_BREITE - 150, BILDSCHIRM_HOEHE // 2))
        self.erz = 0
        self.kapazitaet = 1000


class Tankstelle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bild_laden('tankstelle')
        self.rect = self.image.get_rect(center=(random.randint(50, BILDSCHIRM_BREITE - 50), random.randint(50, BILDSCHIRM_HOEHE - 50)))
