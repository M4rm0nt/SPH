import os
from enum import Enum

import pygame

BILDSCHIRM_BREITE = 800
BILDSCHIRM_HOEHE = 600
FPS = 60
skript_verzeichnis = os.path.dirname(os.path.abspath(__file__))
BILDER_VERZEICHNIS = os.path.join(skript_verzeichnis, "../assets/bilder")
pygame.init()


def init_schriften():
    global SCHRIFT_KLEIN, SCHRIFT_GROSS
    SCHRIFT_KLEIN = pygame.font.SysFont("arial", 25)
    SCHRIFT_GROSS = pygame.font.SysFont("arial", 36)


WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)


class Tasten(Enum):
    LINKS = pygame.K_LEFT
    RECHTS = pygame.K_RIGHT
    OBEN = pygame.K_UP
    UNTEN = pygame.K_DOWN
    A = pygame.K_a
    D = pygame.K_d
    W = pygame.K_w
    S = pygame.K_s
    PAUSE = pygame.K_p


def bild_laden(name):
    pfad = os.path.join(BILDER_VERZEICHNIS, f'{name}.png')
    return pygame.image.load(pfad).convert_alpha()
