import pygame
import sys


class OptionenMenu:
    def __init__(self, bildschirm, uhr, konfiguration):
        self.konfiguration = konfiguration
        self.bildschirm = bildschirm
        self.uhr = uhr
        self.laeuft = True
        self.schrift = pygame.font.Font(None, 32)
        self.button_schrift = pygame.font.Font(None, 24)
        self.lkw_geschwindigkeit = self.konfiguration.lkw_geschwindigkeit
        self.hubschrauber_geschwindigkeit = self.konfiguration.hubschrauber_geschwindigkeit

    def text_zeichnen(self, text, x, y, schrift=None):
        if schrift is None:
            schrift = self.schrift
        text_flaeche = schrift.render(text, True, (0, 0, 0))
        text_rechteck = text_flaeche.get_rect(midtop=(x, y))
        self.bildschirm.blit(text_flaeche, text_rechteck)

    def button_zeichnen(self, button, text, maus_pos):
        button_color = (0, 0, 255) if button.collidepoint(maus_pos) else (100, 100, 255)
        pygame.draw.rect(self.bildschirm, (0, 0, 0), button.inflate(6, 6))
        pygame.draw.rect(self.bildschirm, button_color, button)
        self.text_zeichnen(text, button.centerx, button.centery, self.button_schrift)

    def ausfuehren(self):
        button_breite = 50
        button_hoehe = 50
        abstand_zwischen_buttons = 100
        lkw_increment_button = pygame.Rect(400 - button_breite - abstand_zwischen_buttons // 2, 200, button_breite, button_hoehe)
        lkw_decrement_button = pygame.Rect(400 + abstand_zwischen_buttons // 2, 200, button_breite, button_hoehe)
        hubschrauber_increment_button = pygame.Rect(400 - button_breite - abstand_zwischen_buttons // 2, 300, button_breite, button_hoehe)
        hubschrauber_decrement_button = pygame.Rect(400 + abstand_zwischen_buttons // 2, 300, button_breite, button_hoehe)

        while self.laeuft:
            maus_pos = pygame.mouse.get_pos()
            for ereignis in pygame.event.get():
                if ereignis.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ereignis.type == pygame.KEYDOWN:
                    if ereignis.key == pygame.K_ESCAPE:
                        self.konfiguration.speichern()
                        self.laeuft = False
                elif ereignis.type == pygame.MOUSEBUTTONDOWN:
                    if lkw_increment_button.collidepoint(ereignis.pos):
                        self.konfiguration.lkw_geschwindigkeit = min(self.konfiguration.lkw_geschwindigkeit + 0.5, 10)
                    elif lkw_decrement_button.collidepoint(ereignis.pos):
                        self.konfiguration.lkw_geschwindigkeit = max(self.konfiguration.lkw_geschwindigkeit - 0.5, 1)
                    elif hubschrauber_increment_button.collidepoint(ereignis.pos):
                        self.konfiguration.hubschrauber_geschwindigkeit = min(
                            self.konfiguration.hubschrauber_geschwindigkeit + 0.5, 10)
                    elif hubschrauber_decrement_button.collidepoint(ereignis.pos):
                        self.konfiguration.hubschrauber_geschwindigkeit = max(
                            self.konfiguration.hubschrauber_geschwindigkeit - 0.5, 1)

            self.bildschirm.fill((255, 255, 255))
            self.text_zeichnen("Optionen-Menü - Drücke ESC, um zurückzukehren", 400, 100)
            self.text_zeichnen(f"LKW-Geschwindigkeit: {self.konfiguration.lkw_geschwindigkeit}", 400,
                               265)
            self.text_zeichnen(f"Hubschrauber-Geschwindigkeit: {self.konfiguration.hubschrauber_geschwindigkeit}",
                               400, 365)
            self.button_zeichnen(lkw_increment_button, "+", maus_pos)
            self.button_zeichnen(lkw_decrement_button, "-", maus_pos)
            self.button_zeichnen(hubschrauber_increment_button, "+", maus_pos)
            self.button_zeichnen(hubschrauber_decrement_button, "-", maus_pos)

            pygame.display.flip()
            self.uhr.tick(60)

