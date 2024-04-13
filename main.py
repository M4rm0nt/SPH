import os
import sys
import pygame

from src.menus.menu_main import HauptmenuZustand
from src.einstellungen.konfiguration import SpielKonfiguration

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def bild_laden(name):
    pfad = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/bilder"), f'{name}.png')
    return pygame.image.load(pfad).convert_alpha()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    pygame.init()
    pygame.display.set_caption("ErzCollector")
    bildschirm = pygame.display.set_mode((800, 600))
    uhr = pygame.time.Clock()

    konfiguration_pfad = os.path.join(os.path.dirname(__file__), 'src/einstellungen', 'konfiguration.ini')
    konfiguration = SpielKonfiguration(konfiguration_pfad)
    zustand = HauptmenuZustand(bildschirm, uhr, konfiguration)

    while True:
        ereignisse = pygame.event.get()
        for ereignis in ereignisse:
            if ereignis.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        neuer_zustand = zustand.verarbeite_ereignisse(ereignisse)
        if neuer_zustand == "QUIT":
            pygame.quit()
            sys.exit()
        elif neuer_zustand != zustand:
            zustand = neuer_zustand

        zustand.aktualisiere()
        zustand.zeichne()

        pygame.display.flip()
        uhr.tick(60)


if __name__ == "__main__":
    main()
