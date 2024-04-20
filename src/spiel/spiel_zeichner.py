import pygame


class SpielZeichner:
    def __init__(self, bildschirm):
        self.bildschirm = bildschirm

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

    def zeichne(self, alle_sprites, spiel_laeuft, pause, lkw, hubschrauber, lager, erz_quelle):
        self.bildschirm.fill((255, 255, 255))
        alle_sprites.draw(self.bildschirm)

        balken_breite = self.bildschirm.get_width() // 4
        balken_hoehe = 30
        y_position_oben = 0
        y_position_unten = self.bildschirm.get_height() - balken_hoehe

        if spiel_laeuft:
            if pause:
                self.zeichne_pause_nachricht()
            else:
                self.zeichne_info_balken('Kraftstoff', lkw.kraftstoff, 100, 0, y_position_unten, balken_breite, balken_hoehe, (255, 0, 0), "{:.2f}", "{:.0f}")

                self.zeichne_info_balken('Erz im LKW', lkw.erz, 50, 0 * balken_breite, y_position_oben, balken_breite, balken_hoehe, (0, 255, 0))
                self.zeichne_info_balken('Erz gestohlen', hubschrauber.abgeladenes_erz, 200, 1 * balken_breite, y_position_oben, balken_breite, balken_hoehe, (255, 255, 0))
                self.zeichne_info_balken('Erz im Lager', lager.erz, 800, 2 * balken_breite, y_position_oben, balken_breite, balken_hoehe, (180, 100, 230))
                self.zeichne_info_balken('Erzquelle', erz_quelle.erz_menge, 1000, 3 * balken_breite, y_position_oben, balken_breite, balken_hoehe, (255, 0, 255))
        else:
            self.zeige_endnachricht()

        pygame.display.flip()

    def zeichne_pause_nachricht(self):
        schrift_gross = pygame.font.SysFont("arial", 36)
        text_surface = schrift_gross.render("[PAUSE]", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(400, 300))
        self.bildschirm.blit(text_surface, text_rect)

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

    def zeige_endnachricht(self, endnachricht):
        schrift_gross = pygame.font.SysFont("arial", 36)
        text_surface = schrift_gross.render(endnachricht, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(400, 300))
        self.bildschirm.fill((255, 255, 255))
        self.bildschirm.blit(text_surface, text_rect)
        pygame.display.flip()