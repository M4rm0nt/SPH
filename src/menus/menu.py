import sys
import pygame
from src.components.button import Button
from src.menus.option_menu import OptionenMenu
from src.utilities.einstellungen import BILDSCHIRM_BREITE, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING, START_Y
from src.menus.hilfe_menu import HilfeMenu


class HauptmenuZustand:
    def __init__(self, bildschirm, uhr, konfiguration):
        self.buttons = None
        self.bildschirm = bildschirm
        self.uhr = uhr
        self.konfiguration = konfiguration
        self.schrift_titel = pygame.font.Font(None, 48)
        self.titel_text = "Hauptmenü"
        self.titel_farbe = (0, 0, 0)
        self.init_buttons()
        self.aktuelle_auswahl = 0

    def init_buttons(self):
        button_titles = ["Spielen", "Optionen", "Hilfe", "Beenden"]
        self.buttons = [
            Button(title, (BILDSCHIRM_BREITE - BUTTON_WIDTH) // 2, START_Y + i * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, getattr(self, title.lower()))
            for i, title in enumerate(button_titles)
        ]

    def spielen(self):
        from src.game.spiel import SpielZustand
        return SpielZustand(self.bildschirm, self.uhr, self.konfiguration)

    def optionen(self):
        optionen_menu = OptionenMenu(self.bildschirm, self.uhr, self.konfiguration)
        optionen_menu.ausfuehren()

    def hilfe(self):
        hilfe_menu = HilfeMenu(self.bildschirm, self.uhr)
        hilfe_menu.ausfuehren()

    def beenden(self):
        pygame.quit()
        sys.exit()

    def verarbeite_ereignisse(self, ereignisse):
        for ereignis in ereignisse:
            if ereignis.type == pygame.KEYDOWN:
                if ereignis.key == pygame.K_DOWN:
                    self.aktuelle_auswahl = (self.aktuelle_auswahl + 1) % len(self.buttons)
                elif ereignis.key == pygame.K_UP:
                    self.aktuelle_auswahl = (self.aktuelle_auswahl - 1) % len(self.buttons)
                elif ereignis.key == pygame.K_RETURN:
                    result = self.buttons[self.aktuelle_auswahl].aktion()
                    if result:
                        return result
            elif ereignis.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(self.buttons):
                    if button.rechteck.collidepoint(ereignis.pos):
                        self.aktuelle_auswahl = i
                        result = button.aktion()
                        if result:
                            return result
        return self

    def aktualisiere(self):
        pass

    def zeichne(self):
        self.bildschirm.fill((255, 255, 255))
        titel_surf = self.schrift_titel.render(self.titel_text, True, self.titel_farbe)
        titel_rect = titel_surf.get_rect(center=(BILDSCHIRM_BREITE / 2, 50))
        self.bildschirm.blit(titel_surf, titel_rect)

        for i, button in enumerate(self.buttons):
            if i == self.aktuelle_auswahl:
                button.zeichnen_hervorgehoben(self.bildschirm)
            else:
                button.zeichnen(self.bildschirm)
