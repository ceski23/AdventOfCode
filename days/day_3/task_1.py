from helpers import read_input


def run(geoMap):
    x, y = 0, 0
    trees = 0

    while y < len(geoMap):
        if geoMap[y][x] == '#':
            trees += 1
        x = (x + 3) % len(geoMap[0])
        y += 1

    return trees


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 299


def test_test():
    assert run(read_input('test.txt')) == 7
