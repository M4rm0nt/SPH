import os
import sys
import pygame
from src.utilities.einstellungen import BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE, FPS
from src.menus.menu import HauptmenuZustand
from src.utilities.config import SpielKonfiguration

def main():
    # Einstellung des Arbeitsverzeichnisses auf das Verzeichnis, in dem sich main.py befindet
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Initialisierung von pygame
    pygame.init()
    pygame.display.set_caption("ErzCollector")
    bildschirm = pygame.display.set_mode((BILDSCHIRM_BREITE, BILDSCHIRM_HOEHE))
    uhr = pygame.time.Clock()

    # Erstellung des Pfads zur Konfigurationsdatei relativ zu main.py
    config_path = os.path.join(os.path.dirname(__file__), 'utilities', 'config.ini')
    konfiguration = SpielKonfiguration(config_path)
    zustand = HauptmenuZustand(bildschirm, uhr, konfiguration)

    # Hauptspiel-Schleife
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
