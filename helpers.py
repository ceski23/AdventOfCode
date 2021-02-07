import pathlib
import sys


def read_input(input_path):
    # https://stackoverflow.com/a/51488346
    namespace = sys._getframe(1).f_globals
    directory = pathlib.Path(namespace['__file__']).parent.absolute()
    path = directory.joinpath(input_path)
    return open(path, mode='r').read().splitlines()
