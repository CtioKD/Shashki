import pygame as pg
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, BACKGROUND_MUSIC, MUSIC_EAT, MUSIC_END
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        self.__prepare__music()
        self.__sound_eat = pg.mixer.Sound(MUSIC_EAT)
        self.__sound_end = pg.mixer.Sound(MUSIC_END)

    def __prepare__music(self):
        pg.mixer.music.load(BACKGROUND_MUSIC)
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(-1)

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pg.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        self.__sound_eat.play()
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            self.__sound_end.play()
            print('WHITE победили')
            white = (255, 0, 0)
            green = (0, 255, 0)
            blue = (0, 0, 128)

            X = 800
            Y = 800
            display_surface = pg.display.set_mode((X, Y))

            pg.display.set_caption('Show Text')

            font = pg.font.Font('freesansbold.ttf', 32)

            text = font.render('WHITE Win', True, green)

            textRect = text.get_rect()

            textRect.center = (X // 2, Y // 2)

            while True:

                display_surface.fill(white)

                display_surface.blit(text, textRect)

                for event in pg.event.get():

                    if event.type == pg.QUIT:
                        pg.quit()



                    pg.display.update()
            return WHITE
        elif self.white_left <= 0:
            self.__sound_end.play()
            print('RED победили')
            white = (255, 0, 0)
            green = (0, 255, 0)
            blue = (0, 0, 128)

            X = 800
            Y = 800
            display_surface = pg.display.set_mode((X, Y))

            pg.display.set_caption('Show Text')

            font = pg.font.Font('freesansbold.ttf', 32)

            text = font.render('RED Win', True, green)

            textRect = text.get_rect()

            textRect.center = (X // 2, Y // 2)

            while True:

                display_surface.fill(white)

                display_surface.blit(text, textRect)

                for event in pg.event.get():

                    if event.type == pg.QUIT:
                        pg.quit()

                    pg.display.update()
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row


        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves