import sys

import pygame

from src.spiel.spiel_objekte.erzquelle import Erzquelle
from src.spiel.spiel_objekte.hubschrauber import Hubschrauber
from src.spiel.spiel_objekte.hubschrauberlandeplatz import Hubschrauberlandeplatz
from src.spiel.spiel_objekte.lager import Lager
from src.spiel.spiel_objekte.lkw import LKW
from src.spiel.spiel_objekte.tankstelle import Tankstelle


class SpielZustand:
    def __init__(self, bildschirm, uhr, konfiguration, gespeicherter_zustand=None):
        self.bildschirm = bildschirm
        self.uhr = uhr
        self.konfiguration = konfiguration
        self.gespeicherter_zustand = None
        self.pause = False
        self.endnachricht = ""
        self.spiel_laeuft = True
        self.lkw = None
        self.hubschrauberlandeplatz = None
        self.hubschrauber = None
        self.tankstelle = None
        self.lager = None
        self.erz_quelle = None
        self.alle_sprites = None
        self.hubschrauber_gruppe = None
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
        self.hubschrauberlandeplatz = zustand['hubschrauberlandeplatz']
        self.hubschrauber = zustand['hubschrauber']
        self.tankstelle = zustand['tankstelle']
        self.lager = zustand['lager']
        self.erz_quelle = zustand['erz_quelle']
        self.lkw.geschwindigkeit = self.konfiguration.lkw_geschwindigkeit
        self.hubschrauber.geschwindigkeit = self.konfiguration.hubschrauber_geschwindigkeit
        self.alle_sprites = pygame.sprite.Group()
        self.hubschrauber_gruppe = pygame.sprite.Group()
        self.alle_sprites.add(self.lkw, self.erz_quelle, self.lager, self.tankstelle, self.hubschrauberlandeplatz, self.hubschrauber)
        self.hubschrauber_gruppe.add(self.hubschrauber)

    def initialisiere_spiel(self):
        self.konfiguration.lade_konfiguration()
        lkw_geschwindigkeit = self.konfiguration.lkw_geschwindigkeit
        hubschrauber_geschwindigkeit = self.konfiguration.hubschrauber_geschwindigkeit

        self.lkw = LKW(lkw_geschwindigkeit)
        self.hubschrauberlandeplatz = Hubschrauberlandeplatz()
        self.hubschrauber = Hubschrauber(self.lkw, self.hubschrauberlandeplatz, hubschrauber_geschwindigkeit)

        self.erz_quelle = Erzquelle()
        self.lager = Lager()
        self.tankstelle = Tankstelle()

        self.alle_sprites = pygame.sprite.Group()
        self.hubschrauber_gruppe = pygame.sprite.Group()

        self.alle_sprites.add(self.lkw, self.erz_quelle, self.lager, self.tankstelle, self.hubschrauberlandeplatz,
                              self.hubschrauber)
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

    def zeichne_info_balken(self, titel, wert, max_wert, x, y, balken_breite, balken_hoehe, farbe, wert_format="{:.0f}", max_format="{:.0f}"):
        schriftart = pygame.font.Font(None, 24)
        balken_hintergrund = pygame.Rect(x, y, balken_breite, balken_hoehe)
        pygame.draw.rect(self.bildschirm, (200, 200, 200), balken_hintergrund)
        fuellstand_breite = max(0, min(wert / max_wert, 1)) * balken_breite
        fuellstand = pygame.Rect(x, y, fuellstand_breite, balken_hoehe)
        pygame.draw.rect(self.bildschirm, farbe, fuellstand)
        text_surf = schriftart.render(titel, True, (0, 0, 0))
        self.bildschirm.blit(text_surf, (x + 5, y + 5))

        wert_text = schriftart.render(f'{wert_format.format(wert)}/{max_format.format(max_wert)}', True, (0, 0, 0))
        wert_text_rect = wert_text.get_rect(center=(x + balken_breite - 50, y + balken_hoehe // 2))
        self.bildschirm.blit(wert_text, wert_text_rect)

    def zeichne(self):
        self.bildschirm.fill((255, 255, 255))
        self.alle_sprites.draw(self.bildschirm)

        balken_breite = self.bildschirm.get_width() // 4
        balken_hoehe = 30
        y_position_oben = 0
        y_position_unten = self.bildschirm.get_height() - balken_hoehe

        if self.spiel_laeuft:
            if self.pause:
                self.zeichne_pause_nachricht()
            else:
                self.zeichne_info_balken('Kraftstoff', self.lkw.kraftstoff, 100, 0, y_position_unten, balken_breite, balken_hoehe, (255, 0, 0), "{:.2f}", "{:.0f}")

                self.zeichne_info_balken('Erz im LKW', self.lkw.erz, 50, 0 * balken_breite, y_position_oben, balken_breite, balken_hoehe, (0, 255, 0))
                self.zeichne_info_balken('Erz gestohlen', self.hubschrauber.abgeladenes_erz, 200, 1 * balken_breite, y_position_oben, balken_breite, balken_hoehe, (255, 255, 0))
                self.zeichne_info_balken('Erz im Lager', self.lager.erz, 800, 2 * balken_breite, y_position_oben, balken_breite, balken_hoehe, (0, 0, 255))
                self.zeichne_info_balken('Erzquelle', self.erz_quelle.erz_menge, 1000, 3 * balken_breite, y_position_oben, balken_breite, balken_hoehe, (255, 0, 255))
        else:
            self.zeige_endnachricht()

        pygame.display.flip()

    def ueberpruefe_spielende(self):
        if self.lkw.kraftstoff <= 0 or self.hubschrauber.abgeladenes_erz == 200:
            self.endnachricht = "Verloren. Spiel vorbei! Neu starten? (J/N)"
            self.spiel_laeuft = False
        elif self.lager.erz == 800:
            self.endnachricht = "Gewonnen. Spiel vorbei! Neu starten? (J/N)"
            self.spiel_laeuft = False


    def zeige_endnachricht(self):
        schrift_gross = pygame.font.SysFont("arial", 36)
        text_surface = schrift_gross.render(self.endnachricht, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(400, 300))
        self.bildschirm.fill((255, 255, 255))
        self.bildschirm.blit(text_surface, text_rect)
        pygame.display.flip()

    def zeige_infos(self, infos, y, separate_info=None):
        schrift_klein = pygame.font.SysFont("arial", 25)
        bildschirm_breite = self.bildschirm.get_size()[0]

        gesamt_breite = sum(schrift_klein.size(info)[0] + 10 for info in infos) - 10

        x_start = (bildschirm_breite - gesamt_breite) // 2

        for info in infos:
            text_surf = schrift_klein.render(info, True, (0, 0, 0))
            text_rect = text_surf.get_rect(left=x_start, top=y)
            self.bildschirm.blit(text_surf, text_rect)
            x_start += text_surf.get_width() + 10

        if separate_info:
            text_surf = schrift_klein.render(separate_info, True, (255, 0, 0))
            text_rect = text_surf.get_rect(midbottom=(bildschirm_breite // 2, self.bildschirm.get_size()[1] - 30))
            self.bildschirm.blit(text_surf, text_rect)

    def zeichne_pause_nachricht(self):
        schrift_gross = pygame.font.SysFont("arial", 36)
        text_surface = schrift_gross.render("[PAUSE]", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(400, 300))
        self.bildschirm.blit(text_surface, text_rect)
        