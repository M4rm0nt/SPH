import sys
import pygame
from src.einstellungen import BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE, FPS
from src.components.menu import HauptmenuZustand
from src.config import SpielKonfiguration


def main():
    pygame.init()
    bildschirm = pygame.display.set_mode((BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE))
    pygame.display.set_caption("ErzCollector")
    uhr = pygame.time.Clock()

    konfiguration = SpielKonfiguration('config.ini')
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
        uhr.tick(FPS)


if __name__ == "__main__":
    main()