import sys

import pygame

from src.spiel.spiel_objekte.erzquelle import Erzquelle
from src.spiel.spiel_objekte.hubschrauber import Hubschrauber
from src.spiel.spiel_objekte.hubschrauberlandeplatz import Hubschrauberlandeplatz
from src.spiel.spiel_objekte.lager import Lager
from src.spiel.spiel_objekte.lkw import LKW
from src.spiel.spiel_objekte.tankstelle import Tankstelle
from src.spiel.spiel_zeichner import SpielZeichner


class SpielZustand:
    def __init__(self, bildschirm, uhr, konfiguration, gespeicherter_zustand=None):
        self.bildschirm = bildschirm
        self.uhr = uhr
        self.konfiguration = konfiguration
        self.spiel_laeuft = True
        self.pause = False
        self.gespeicherter_zustand = None
        self.lkw = None
        self.hubschrauberlandeplatz = None
        self.hubschrauber = None
        self.tankstelle = None
        self.lager = None
        self.erz_quelle = None
        self.alle_sprites = None
        self.hubschrauber_gruppe = None
        self.endnachricht = ""
        self.zeichner = SpielZeichner(bildschirm)
        if gespeicherter_zustand:
            self.lade_zustand(gespeicherter_zustand)
        else:
            self.initialisiere_spiel()

    def speichern_zustand(self):
        self.gespeicherter_zustand = {
            'lkw': self.lkw,
            'hubschrauberlandeplatz': self.hubschrauberlandeplatz,
            'hubschrauber': self.hubschrauber,
            'tankstelle': self.tankstelle,
            'lager': self.lager,
            'erz_quelle': self.erz_quelle
        }
        return self.gespeicherter_zustand

    def lade_zustand(self, zustand):
        self.konfiguration.lade_konfiguration()
        self.lkw = zustand['lkw']
        self.lkw.geschwindigkeit = self.konfiguration.lkw_geschwindigkeit
        self.hubschrauber = zustand['hubschrauber']
        self.hubschrauber.geschwindigkeit = self.konfiguration.hubschrauber_geschwindigkeit
        self.hubschrauberlandeplatz = zustand['hubschrauberlandeplatz']
        self.tankstelle = zustand['tankstelle']
        self.lager = zustand['lager']
        self.erz_quelle = zustand['erz_quelle']
        self.alle_sprites = pygame.sprite.Group()
        self.hubschrauber_gruppe = pygame.sprite.Group()
        self.alle_sprites.add(self.lkw, self.erz_quelle, self.lager, self.tankstelle, self.hubschrauberlandeplatz, self.hubschrauber)
        self.hubschrauber_gruppe.add(self.hubschrauber)

    def initialisiere_spiel(self):
        self.konfiguration.lade_konfiguration()

        lkw_geschwindigkeit = self.konfiguration.lkw_geschwindigkeit
        self.lkw = LKW(lkw_geschwindigkeit)

        hubschrauber_geschwindigkeit = self.konfiguration.hubschrauber_geschwindigkeit
        self.hubschrauberlandeplatz = Hubschrauberlandeplatz()
        self.hubschrauber = Hubschrauber(self.lkw, self.hubschrauberlandeplatz, hubschrauber_geschwindigkeit)

        self.erz_quelle = Erzquelle()
        self.lager = Lager()
        self.tankstelle = Tankstelle()

        self.alle_sprites = pygame.sprite.Group()
        self.alle_sprites.add(self.lkw, self.erz_quelle, self.lager, self.tankstelle, self.hubschrauberlandeplatz,
                              self.hubschrauber)
        self.hubschrauber_gruppe = pygame.sprite.Group()
        self.hubschrauber_gruppe.add(self.hubschrauber)

    def verarbeite_ereignisse(self, ereignisse):
        for ereignis in ereignisse:
            if ereignis.type == pygame.KEYDOWN:
                if self.spiel_laeuft:
                    if ereignis.key == pygame.K_ESCAPE:
                        gespeicherter_zustand = self.speichern_zustand()
                        from src.menus.menu_main import HauptmenuZustand
                        return HauptmenuZustand(self.bildschirm, self.uhr, self.konfiguration, gespeicherter_zustand)
                    elif ereignis.key == pygame.K_p:
                        self.pause = not self.pause
                if ereignis.key == pygame.K_j:
                    if not self.spiel_laeuft:
                        self.initialisiere_spiel()
                        self.spiel_laeuft = True
                        return self
                elif ereignis.key == pygame.K_n:
                    if not self.spiel_laeuft:
                        pygame.quit()
                        sys.exit()
        return self

    def aktualisiere(self):
        if self.spiel_laeuft and not self.pause:
            tasten = pygame.key.get_pressed()
            self.lkw.update(tasten, self.erz_quelle, self.lager, self.tankstelle, self.hubschrauber_gruppe)
            self.hubschrauber_gruppe.update()
            self.ueberpruefe_spielende()

    def zeichne(self):
        if self.spiel_laeuft:
            self.zeichner.zeichne(self.alle_sprites, self.spiel_laeuft, self.pause, self.lkw, self.hubschrauber,
                                  self.lager, self.erz_quelle)
        else:
            self.zeichner.zeige_endnachricht(self.endnachricht)

    def ueberpruefe_spielende(self):
        if self.lkw.kraftstoff <= 0 or self.hubschrauber.abgeladenes_erz == 200:
            self.endnachricht = "Verloren. Spiel vorbei! Neu starten? (J/N)"
            self.spiel_laeuft = False
        elif self.lager.erz == 800:
            self.endnachricht = "Gewonnen. Spiel vorbei! Neu starten? (J/N)"
            self.spiel_laeuft = False

    def zeige_endnachricht(self):
        self.zeichner.zeige_endnachricht(self.endnachricht)
