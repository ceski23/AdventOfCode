from helpers import read_input
from days.day_15.task_1 import nth_spoken_number


def run(data):
    numbers = [int(n) for n in data[0].split(',')]
    return nth_spoken_number(numbers, 30000000)


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 814
