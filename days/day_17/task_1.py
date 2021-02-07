from helpers import read_input
from itertools import product


def get_neighbours(pos):
    neighbours = set()

    for shift in product(*[range(-1, 2)] * len(pos)):
        if sum([abs(x) for x in shift]) != 0:
            neighbours.add(tuple(map(sum, zip(pos, shift))))

    return neighbours


def count_active(cubes, pos):
    active_count = 0
    neighbours = get_neighbours(pos)

    for cube_pos in neighbours:
        if neighbour := cubes.get(cube_pos):
            if neighbour == '#':
                active_count += 1

    return active_count


def tick(cubes):
    changes = {}
    active_neighbours = {}

    for cube in cubes:
        if cubes[cube] == '#':
            active = count_active(cubes, cube)

            neighbours = get_neighbours(cube)
            for n in neighbours:
                if n not in active_neighbours:
                    active_neighbours[n] = 0
                active_neighbours[n] += 1

            if active != 2 and active != 3:
                changes[cube] = '.'

    for pos, active in active_neighbours.items():
        if (cubes.get(pos) == None or cubes[pos] == '.') and active == 3:
            changes[pos] = '#'

    for pos, state in changes.items():
        cubes[pos] = state

    return cubes


def run(data):
    cubes = {}

    for y, row in enumerate(data):
        for x, column in enumerate(row):
            cubes[(x, y, 0)] = column

    for _ in range(6):
        cubes = tick(cubes)

    return sum([1 if state == '#' else 0 for state in cubes.values()])


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 271


def test_test():
    assert run(read_input('test.txt')) == 112
