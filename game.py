import pygame, sys, random
from pygame.locals import *
import numpy as np

# Config
GRID_SIZE = 4
TILE_SIZE = 110
PADDING = 10
WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * PADDING
HEIGHT = WIDTH + 100
FPS = 60
FONT_NAME = None  # default

# Colors
BG_COLOR = (187, 173, 160)
EMPTY_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TEXT_COLOR = (119, 110, 101)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 RL")
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_NAME, 36)
small_font = pygame.font.Font(FONT_NAME, 20)
