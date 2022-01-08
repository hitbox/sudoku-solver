import argparse

from framework.engine import Engine
from framework.pygame import pygame

class Test:

    def start(self):
        pass

    def update(self):
        pass


def start(engine):
    print('starting')

def update(engine):
    print('running')
    print('stopping')
    engine.quit()

def main(argv=None):
    """
    Testing this framework thing I'm sketching out.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    args = parser.parse_args(argv)

    test = Test()
    engine = Engine.from_object(test)
    engine.run()

if __name__ == '__main__':
    main()
