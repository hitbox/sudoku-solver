from framework import render
from framework import style
from framework.pygame import pygame
from framework.screen import Screen

def init_style():
    style.set('framework.render.box', 'background.color', (200,10,10))
    style.set('framework.render.box', 'border.color', (200,)*3)
    #
    style.set('sudoku.cell', 'size', (16,)*2)
    style.set('sudoku.cell', 'background.color', (10,10,200))
    style.set('sudoku.cell', 'border.color', (200,)*3)
    style.set('sudoku.cell', 'border.width', 1)

class SudokuBoardGUI:
    """
    The main Sudoku GUI interface.
    """

    def __init__(self, engine):
        self.engine = engine
        self.screen = None

    def start(self):
        init_style()
        self.screen = Screen((320, 200), scale=4)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.engine.stop()
            # separate object to handle events?
        # draw
        self.screen.clear()
        image = render.box('sudoku.cell')
        rect = image.get_rect(center=self.screen.rect.center)
        self.screen.surface.blit(image, rect)
        # update
        self.screen.update()
