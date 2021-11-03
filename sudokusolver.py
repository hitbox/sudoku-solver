import argparse
import os

from contextlib import redirect_stdout
from itertools import zip_longest

with redirect_stdout(open(os.devnull, 'w')):
    import pygame

NUMBERS = set(range(1,10))
FRAMERATE = 60

def parse_file(fp):
    board = []
    for line in fp.readlines():
        if set(line) == set('-+\n'):
            continue
        row = [0 if c == ' ' else int(c) for c in line if c.isdigit() or c == ' ']
        if len(row) != 9:
            raise ValueError
        board.append(row)
    if len(board) != 9:
        raise ValueError
    return board

def is_solved(board):
    for row in board:
        if set(row).isdisjoint(NUMBERS):
            return False

    columns = zip(*board)
    for col in columns:
        if set(col).isdisjoint(NUMBERS):
            return False

    for y in range(0, 9, 3):
        for x in range(0, 9, 3):
            cells = []
            for i in range(3):
                for j in range(3):
                    cells.append(board[y+i][x+j])
            if len(cells) != 9:
                raise ValueError
            if set(cells).isdisjoint(NUMBERS):
                return False

def column(board, col):
    by_cols = list(zip(*board))
    return by_cols[col]

def gridcells(board, y, x):
    t = y // 3
    l = x // 3
    cells = []
    for i in range(3):
        for j in range(3):
            cells.append(board[t+i][l+j])
    if len(cells) != 9:
        raise ValueError
    return cells

def get_entropy(board):
    entropy = dict()
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == 0:
                colcells = column(board, x)
                gcells = gridcells(board, y, x)
                exists = set(row).union(colcells).union(gcells)
                possible = set(NUMBERS).difference(exists)
                if not possible:
                    raise ValueError
                entropy[(x,y)] = possible
    return entropy

def temp():
    with open(args.board) as fp:
        board = parse_file(fp)

    from pprint import pprint
    pprint(board)
    while not is_solved(board):
        entropy = get_entropy(board)
        pprint(entropy)
        #break
        pos = min(entropy, default=0, key=lambda key: len(entropy[key]))
        x, y = pos
        board[y][x] = entropy[pos].pop()
        pprint(board)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('boardfile')
    args = parser.parse_args(argv)

    with open(args.boardfile) as fp:
        board = parse_file(fp)

    pygame.display.init()
    pygame.font.init()

    screen = pygame.display.set_mode((500,400))
    frame = screen.get_rect()
    background = screen.copy()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)

    entropy = None
    running = True
    while running:
        elapsed = clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key == pygame.K_SPACE:
                    if not is_solved(board):
                        entropy = get_entropy(board)
                        pos = min(entropy, default=0, key=lambda key: len(entropy[key]))
                        x, y = pos
                        board[y][x] = entropy[pos].pop()
        # draw
        screen.blit(background, (0, 0))
        texts = [str(cell) for row in board for cell in row]
        size = max(font.size(text) for text in texts)
        images = [font.render(text, True, (200,10,10)) for text in texts]
        for y, image in enumerate(images):
            pos = (y % 9 * size[0], y // 9 * size[1])
            screen.blit(image, pos)
        #
        if entropy:
            for y, item in enumerate(entropy.items()):
                image = font.render(f'{item}', True, (200,10,10))
                screen.blit(image, image.get_rect(y=y*40, right=frame.right))
        pygame.display.flip()

if __name__ == '__main__':
    main()
