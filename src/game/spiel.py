import pygame

from src.objects.erzquelle import Erzquelle
from src.objects.hubschrauber import Hubschrauber
from src.objects.hubschrauberlandeplatz import Hubschrauberlandeplatz
from src.objects.lager import Lager
from src.objects.lkw import LKW
from src.objects.tankstelle import Tankstelle
from src.utilities.einstellungen import BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE


class SpielZustand:
    def __init__(self, bildschirm, uhr, konfiguration):
        self.konfiguration = konfiguration
        self.bildschirm = bildschirm
        self.uhr = uhr
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
        self.initialisiere_spiel()

    def initialisiere_spiel(self):
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
        if self.spiel_laeuft:
            for ereignis in ereignisse:
                if ereignis.type == pygame.KEYDOWN:
                    if ereignis.key == pygame.K_ESCAPE:
                        from src.menus.menu import HauptmenuZustand
                        return HauptmenuZustand(self.bildschirm, self.uhr, self.konfiguration)
                    elif ereignis.key == pygame.K_p:
                        self.pause = not self.pause
        else:
            for ereignis in ereignisse:
                if ereignis.type == pygame.KEYDOWN:
                    if ereignis.key == pygame.K_j:
                        self.initialisiere_spiel()
                        self.spiel_laeuft = True
                    elif ereignis.key == pygame.K_n:
                        return "QUIT"
                elif ereignis.type == pygame.QUIT:
                    return "QUIT"
        return self

    def aktualisiere(self):
        if self.spiel_laeuft and not self.pause:
            tasten = pygame.key.get_pressed()
            self.lkw.update(tasten, self.erz_quelle, self.lager, self.tankstelle, self.hubschrauber_gruppe)
            self.hubschrauber_gruppe.update()
            self.ueberpruefe_spielende()

    def zeichne(self):
        self.bildschirm.fill((255, 255, 255))
        self.alle_sprites.draw(self.bildschirm)

        if self.spiel_laeuft:
            if self.pause:
                self.zeichne_pause_nachricht()
            else:
                info_liste = [
                    f'Sprit: {int(self.lkw.kraftstoff)}',
                    f'Erz im LKW: {self.lkw.erz}',
                    f'Erz am Lager: {self.lager.erz}/{self.lager.kapazitaet}'
                ]
                self.zeige_infos(info_liste, 20, separate_info=f'Erz gestohlen: {self.hubschrauber.abgeladenes_erz}')
        else:
            self.zeige_endnachricht()

        pygame.display.flip()

    def ueberpruefe_spielende(self):
        if self.lkw.kraftstoff <= 0 or self.hubschrauber.abgeladenes_erz > 200:
            self.endnachricht = "Verloren. Spiel vorbei! Neu starten? (J/N)"
            self.spiel_laeuft = False
        elif self.lager.erz > 800:
            self.endnachricht = "Gewonnen. Spiel vorbei! Neu starten? (J/N)"
            self.spiel_laeuft = False
        elif self.lager.erz == 800 and self.hubschrauber.abgeladenes_erz >= 200:
            self.endnachricht = "Unentschieden. Spiel vorbei! Neu starten? (J/N)"
            self.spiel_laeuft = False

    def zeige_endnachricht(self):
        schrift_gross = pygame.font.SysFont("arial", 36)
        text_surface = schrift_gross.render(self.endnachricht, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(BILDSCHIRM_BREITE / 2, BILDSCHIRM_HOEHE / 2))
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
        text_rect = text_surface.get_rect(center=(BILDSCHIRM_BREITE / 2, BILDSCHIRM_HOEHE / 2))
        self.bildschirm.blit(text_surface, text_rect)
        