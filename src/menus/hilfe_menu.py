import pygame
import sys
from src.game.einstellungen import BILDSCHIRM_BREITE


class HilfeMenu:
    def __init__(self, bildschirm, uhr):
        self.bildschirm = bildschirm
        self.uhr = uhr
        self.laeuft = True
        self.schrift = pygame.font.Font(None, 32)

    def text_zeichnen(self, text, x, y):
        text_flaeche = self.schrift.render(text, True, (0, 0, 0))
        text_rechteck = text_flaeche.get_rect(center=(x, y))
        self.bildschirm.blit(text_flaeche, text_rechteck)

    def ausfuehren(self):
        while self.laeuft:
            for ereignis in pygame.event.get():
                if ereignis.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ereignis.type == pygame.KEYDOWN:
                    if ereignis.key == pygame.K_ESCAPE:
                        self.laeuft = False

            self.bildschirm.fill((255, 255, 255))
            self.text_zeichnen("Hilfe-Menü - Drücke ESC, um zurückzukehren", BILDSCHIRM_BREITE // 2, 100)
            self.text_zeichnen("Steuerung", BILDSCHIRM_BREITE // 2, 150)
            self.text_zeichnen("W-A-S-D oder Pfeiltasten zum steuern des LKW", BILDSCHIRM_BREITE // 2, 175)
            self.text_zeichnen("Ziel:", BILDSCHIRM_BREITE // 2, 225)
            self.text_zeichnen("Bringe das Erz zum Ablageort", BILDSCHIRM_BREITE // 2, 250)
            self.text_zeichnen("Achte auf den Hellikopter!", BILDSCHIRM_BREITE // 2, 275)

            pygame.display.flip()
            self.uhr.tick(60)
