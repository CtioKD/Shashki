import pygame as pg

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pg.transform.scale(pg.image.load('assets/crown.png'), (44, 25))
BACKGROUND_MUSIC = 'assets/back.mp3'
MUSIC_STUP = 'assets/shag.mp3'
MUSIC_EAT = 'assets/eat.mp3'
MUSIC_END = 'assets/the_end.mp3'
