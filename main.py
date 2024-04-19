import os
import random
import sys
import pygame

from src.einstellungen.konfiguration import SpielKonfiguration

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def bild_laden(name):
    basispfad = os.path.dirname(os.path.abspath(__file__))
    bildpfad = os.path.join(basispfad, "ressourcen", "bilder", f"{name}.png")

    if not os.path.exists(bildpfad):
        raise FileNotFoundError(f"Das Bild {bildpfad} konnte nicht gefunden werden.")

    try:
        bild = pygame.image.load(bildpfad).convert_alpha()
        return bild
    except pygame.error as e:
        raise IOError(f"Fehler beim Laden des Bildes {name}.png: {e}")


def platziere_objekte_sicher(anzahl_objekte, bereich_breite, bereich_hoehe, mindestabstand):
    platzierte_positionen = []
    for _ in range(anzahl_objekte):
        while True:
            x = random.randint(0, bereich_breite)
            y = random.randint(0, bereich_hoehe)
            abstand_ok = all(abs(x - pos[0]) > mindestabstand or abs(y - pos[1]) > mindestabstand for pos in platzierte_positionen)
            if abstand_ok:
                platzierte_positionen.append((x, y))
                break
    return platzierte_positionen


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    pygame.init()
    pygame.display.set_caption("ErzCollector")
    bildschirm = pygame.display.set_mode((800, 600))
    uhr = pygame.time.Clock()

    konfiguration_pfad = os.path.join(os.path.dirname(__file__), 'src/einstellungen', 'konfiguration.ini')
    konfiguration = SpielKonfiguration(konfiguration_pfad)
    from src.menus.menu_main import HauptmenuZustand
    zustand = HauptmenuZustand(bildschirm, uhr, konfiguration)

    while True:
        ereignisse = pygame.event.get()
        for ereignis in ereignisse:
            if ereignis.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        from src.spiel.spiel_zustand import SpielZustand
        neuer_zustand = zustand.verarbeite_ereignisse(ereignisse)
        if isinstance(neuer_zustand, SpielZustand) or isinstance(neuer_zustand, HauptmenuZustand):
            if neuer_zustand != zustand:
                zustand = neuer_zustand

        zustand.aktualisiere()
        zustand.zeichne()
        pygame.display.flip()
        uhr.tick(60)


if __name__ == "__main__":
    main()
