import curses
import random
import time

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

SHAPES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    'O': [
        [[1, 1],
         [1, 1]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0],
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]]
    ]
}

TICK = 0.5  # time between automatic drops

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.rotation = 0
        self.x = BOARD_WIDTH // 2 - len(self.current()[0]) // 2
        self.y = 0

    def current(self):
        return SHAPES[self.shape][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPES[self.shape])


def create_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def can_move(board, tetro, dx, dy, rotation=None):
    if rotation is None:
        rotation = tetro.rotation
    shape = SHAPES[tetro.shape][rotation]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx = tetro.x + x + dx
                ny = tetro.y + y + dy
                if nx < 0 or nx >= BOARD_WIDTH or ny >= BOARD_HEIGHT:
                    return False
                if ny >= 0 and board[ny][nx]:
                    return False
    return True


def place_piece(board, tetro):
    shape = tetro.current()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                ny = tetro.y + y
                nx = tetro.x + x
                if 0 <= ny < BOARD_HEIGHT and 0 <= nx < BOARD_WIDTH:
                    board[ny][nx] = 1


def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = BOARD_HEIGHT - len(new_board)
    while len(new_board) < BOARD_HEIGHT:
        new_board.insert(0, [0] * BOARD_WIDTH)
    return new_board, cleared


def draw_board(stdscr, board, tetro, score):
    stdscr.clear()
    for y, row in enumerate(board):
        line = ''
        for x, cell in enumerate(row):
            if cell:
                line += '#'
            else:
                line += ' '
        stdscr.addstr(y, 0, line)

    shape = tetro.current()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                ny = tetro.y + y
                nx = tetro.x + x
                if 0 <= ny < BOARD_HEIGHT and 0 <= nx < BOARD_WIDTH:
                    stdscr.addstr(ny, nx, '#')

    stdscr.addstr(0, BOARD_WIDTH + 2, f"Score: {score}")
    stdscr.refresh()


def game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    board = create_board()
    current = Tetromino(random.choice(list(SHAPES.keys())))
    last_drop = time.time()
    score = 0

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT and can_move(board, current, -1, 0):
            current.x -= 1
        elif key == curses.KEY_RIGHT and can_move(board, current, 1, 0):
            current.x += 1
        elif key == curses.KEY_DOWN and can_move(board, current, 0, 1):
            current.y += 1
        elif key == curses.KEY_UP:
            new_rotation = (current.rotation + 1) % len(SHAPES[current.shape])
            if can_move(board, current, 0, 0, new_rotation):
                current.rotate()

        if time.time() - last_drop > TICK:
            if can_move(board, current, 0, 1):
                current.y += 1
            else:
                place_piece(board, current)
                board, cleared = clear_lines(board)
                score += cleared
                current = Tetromino(random.choice(list(SHAPES.keys())))
                if not can_move(board, current, 0, 0):
                    break
            last_drop = time.time()

        draw_board(stdscr, board, current, score)
        time.sleep(0.05)

    stdscr.nodelay(False)
    stdscr.addstr(BOARD_HEIGHT // 2, BOARD_WIDTH // 2 - 5, "GAME OVER")
    stdscr.addstr(BOARD_HEIGHT // 2 + 1, BOARD_WIDTH // 2 - 7, f"Final Score: {score}")
    stdscr.refresh()
    stdscr.getch()


def main():
    curses.wrapper(game)

if __name__ == '__main__':
    main()
