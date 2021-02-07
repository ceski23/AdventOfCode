from helpers import read_input


class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 90  # east

    def move(self, units, direction=None):
        if direction == None:
            direction = self.direction
        if direction == 0:
            self.y += units
        elif direction == 90:
            self.x += units
        elif direction == 180:
            self.y -= units
        elif direction == 270:
            self.x -= units

    def turn(self, degrees):
        self.direction = (self.direction + degrees) % 360


def direction_to_degree(direction):
    if direction == 'N':
        return 0
    elif direction == 'E':
        return 90
    elif direction == 'S':
        return 180
    elif direction == 'W':
        return 270


def run(data):
    instructions = [(line[0], int(line[1:])) for line in data]

    ship = Ship()
    for ins, units in instructions:
        if ins == 'F':
            ship.move(units)
        elif ins in ['N', 'S', 'E', 'W']:
            ship.move(units, direction_to_degree(ins))
        elif ins == 'L':
            ship.turn(-units)
        elif ins == 'R':
            ship.turn(units)

    return abs(ship.x) + abs(ship.y)


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 2879


def test_test():
    assert run(read_input('test.txt')) == 25
