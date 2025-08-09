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

def new_board():
    board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    add_random_tile(board)
    add_random_tile(board)
    return board

def add_random_tile(board):
    empties = [(r,c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c]==0]
    if not empties: return
    r,c = random.choice(empties)
    board[r][c] = 4 if random.random() < 0.1 else 2

def transpose(board):
    return [list(row) for row in zip(*board)]

def reverse(board):
    return [list(reversed(row)) for row in board]

def compress(row):
    new = [v for v in row if v!=0]
    new += [0]*(GRID_SIZE - len(new))
    return new

def merge(row):
    score = 0
    for i in range(GRID_SIZE-1):
        if row[i] != 0 and row[i] == row[i+1]:
            row[i] *= 2
            score += row[i]
            row[i+1] = 0
    return row, score

def move_left(board):
    moved = False
    score = 0
    new_board = []
    for row in board:
        compressed = compress(row)
        merged, s = merge(compressed)
        compressed_again = compress(merged)
        new_board.append(compressed_again)
        if compressed_again != row: moved = True
        score += s
    return new_board, moved, score

def move_right(board):
    rev = reverse(board)
    moved_board, moved, score = move_left(rev)
    return reverse(moved_board), moved, score

def move_up(board):
    trans = transpose(board)
    moved_board, moved, score = move_left(trans)
    return transpose(moved_board), moved, score

def move_down(board):
    trans = transpose(board)
    moved_board, moved, score = move_right(trans)
    return transpose(moved_board), moved, score

def can_move(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c]==0: return True
            if c+1<GRID_SIZE and board[r][c]==board[r][c+1]: return True
            if r+1<GRID_SIZE and board[r][c]==board[r+1][c]: return True
    return False

def draw_board(board, score):
    screen.fill(BG_COLOR)
    title_surf = font.render("2048", True, TEXT_COLOR)
    screen.blit(title_surf, (PADDING, HEIGHT - 90))
    score_surf = small_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_surf, (WIDTH - 150, HEIGHT - 82))
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            x = PADDING + c*(TILE_SIZE + PADDING)
            y = PADDING + r*(TILE_SIZE + PADDING)
            val = board[r][c]
            rect = pygame.Rect(x,y,TILE_SIZE,TILE_SIZE)
            color = TILE_COLORS.get(val, EMPTY_COLOR) if val!=0 else EMPTY_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=8)
            if val:
                text_color = (249,246,242) if val >= 8 else TEXT_COLOR
                txt = font.render(str(val), True, text_color)
                txt_rect = txt.get_rect(center=rect.center)
                screen.blit(txt, txt_rect)