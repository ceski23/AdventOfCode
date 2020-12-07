import math


def checkSlope(geoMap, right, down):
    x, y = 0, 0
    trees = 0

    while y < len(geoMap):
        if geoMap[y][x] == '#':
            trees += 1
        x = (x + right) % len(geoMap[0])
        y += down

    return trees


def run():
    with open('inputs/3.txt') as f:
        geoMap = f.read().splitlines()
        slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
        numbers = [checkSlope(geoMap, *slope) for slope in slopes]
        return math.prod(numbers)


if __name__ == "__main__":
    print(run())
