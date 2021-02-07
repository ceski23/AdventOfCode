from helpers import read_input
from days.day_17.task_1 import tick


def run(data):
    cubes = {}

    for y, row in enumerate(data):
        for x, column in enumerate(row):
            cubes[(x, y, 0, 0)] = column

    for _ in range(6):
        cubes = tick(cubes)

    return sum([1 if state == '#' else 0 for state in cubes.values()])


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 2064


def test_test():
    assert run(read_input('test.txt')) == 848
