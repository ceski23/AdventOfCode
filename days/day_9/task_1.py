from helpers import read_input
from days.day_1.task_1 import findTwo


def run(data, preamble_size):
    numbers = []
    for line in data:
        number = int(line)
        if len(numbers) > preamble_size and not findTwo(numbers[-preamble_size:], number):
            return number
        numbers.append(number)


if __name__ == "__main__":
    print(run(read_input('input.txt'), 25))


def test_input():
    assert run(read_input('input.txt'), 25) == 675280050


def test_test():
    assert run(read_input('test.txt'), 5) == 127
