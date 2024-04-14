import pygame


class Button:
    def __init__(self, text, x, y, breite, hoehe, aktion, schrift_groesse=32, farbe=(255, 255, 255), hover_farbe=(200, 200, 200), hervorgehoben_farbe=(255, 255, 0), text_farbe=(0, 0, 0)):
        self.text = text
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.aktion = aktion
        self.farbe = farbe
        self.hover_farbe = hover_farbe
        self.hervorgehoben_farbe = hervorgehoben_farbe
        self.text_farbe = text_farbe
        self.schrift = pygame.font.Font(None, schrift_groesse)
        self.rechteck = pygame.Rect(x, y, breite, hoehe)

    def zeichnen(self, bildschirm):
        maus_pos = pygame.mouse.get_pos()
        button_farbe = self.hover_farbe if self.rechteck.collidepoint(maus_pos) else self.farbe
        pygame.draw.rect(bildschirm, button_farbe, self.rechteck)

        text_flaeche = self.schrift.render(self.text, True, self.text_farbe)
        text_rechteck = text_flaeche.get_rect(center=self.rechteck.center)
        bildschirm.blit(text_flaeche, text_rechteck)

    def zeichnen_hervorgehoben(self, bildschirm):
        pygame.draw.rect(bildschirm, self.hervorgehoben_farbe, self.rechteck)
        pygame.draw.rect(bildschirm, (0, 0, 0), self.rechteck, 2)

        text_flaeche = self.schrift.render(self.text, True, self.text_farbe)
        text_rechteck = text_flaeche.get_rect(center=self.rechteck.center)
        bildschirm.blit(text_flaeche, text_rechteck)

    def ereignis_behandeln(self, ereignis):
        if ereignis.type == pygame.MOUSEBUTTONDOWN:
            if self.rechteck.collidepoint(ereignis.pos):
                self.aktion()
