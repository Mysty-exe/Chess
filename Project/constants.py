import pygame

pygame.font.init()

TITLE = "Chess"
ICON = "Assets\\icon.png"
WIDTH = 1000
HEIGHT = 600
FPS = 60
COLOURS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "light red": (100, 28, 30),
    "red": (139, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 220, 0),
    "green": (0, 255, 0),
    "blue": (10, 52, 99),
    "indigo": (75, 0, 130),
    "magenta": (255, 0, 255),
    "lime": (118, 186, 27),
    "grey": (24, 25, 26),
    "light grey": (211, 211, 211),
    "light blue": (173, 216, 230),
    "red2": (229, 57, 53),
    "light purple": (84, 71, 99),
    "purple": (40, 1, 55),
    "gold": (255, 218, 0)
}
PIECES = {
    "p1": ("a2", "a7"), "p2": ("b2", "b7"), "p3": ("c2", "c7"), "p4": ("d2", "d7"), "p5": ("e2", "e7"), "p6": ("f2", "f7"), "p7": ("g2", "g7"), "p8": ("h2", "h7"), "r1": ("a1", "a8"), "k1": ("b1", "b8"), "b1": ("c1", "c8"), "q": ("d1", "d8"), "king": ("e1", "e8"), "b2": ("f1", "f8"), "k2": ("g1", "g8"), "r2": ("h1", "h8")
}
REFLECTED = {
    1:8,
    2:7,
    3:6,
    4:5,
    5:4,
    6:3,
    7:2,
    8:1
}

biggerFont = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 136)
bigFont = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 112)
font = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 64)
medfont = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 36)
regFont = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 24)
smallFont = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 18)
