import pygame as pg
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED
from checkers.game import Game
import pygame_menu


FPS = 144

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Checkers')



#Экран + меню

pg.init()
surface = pg.display.set_mode((WIDTH, HEIGHT))

def start_the_game():
    run = True
    clock = pg.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


menu = pygame_menu.Menu('Приветствую в игре шашки', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_ORANGE)

menu.add.button('Работа Kirillа')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)





