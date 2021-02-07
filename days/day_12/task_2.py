from helpers import read_input
import math


class Object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 0

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


class Waypoint(Object):
    def __init__(self):
        super().__init__()
        self.x = 10
        self.y = 1

    def rotate(self, degrees):
        s = int(math.sin(math.radians(degrees)))
        c = int(math.cos(math.radians(degrees)))

        new_x = self.x * c - self.y * s
        new_y = self.x * s + self.y * c

        self.x = new_x
        self.y = new_y


class Ship(Object):
    def __init__(self):
        super().__init__()
        self.direction = direction_to_degree('E')
        self.waypoint = Waypoint()


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
            ship.move(ship.waypoint.x * units, direction_to_degree('E'))
            ship.move(ship.waypoint.y * units, direction_to_degree('N'))
        elif ins in ['N', 'S', 'E', 'W']:
            ship.waypoint.move(units, direction_to_degree(ins))
        elif ins == 'L':
            ship.waypoint.rotate(units)
        elif ins == 'R':
            ship.waypoint.rotate(-units)

    return abs(ship.x) + abs(ship.y)


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 178986


def test_test():
    assert run(read_input('test.txt')) == 286
