from framework.engine import Engine

from .sudoku_board_gui import SudokuBoardGUI

def run():
    """
    Run main Sudoku board GUI.
    """
    # XXX: each refering to each other
    engine = Engine()
    gui = SudokuBoardGUI(engine)
    engine.start = gui.start
    engine.update = gui.update
    engine.run()
