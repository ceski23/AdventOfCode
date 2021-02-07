from helpers import read_input


def findTwo(numbers, x):
    diffs = {}
    for number in numbers:
        if diffs.get(number):
            return [number, diffs.get(number)]
        diffs[x - number] = number


def run(data):
    numbers = [int(x) for x in data]
    a, b = findTwo(numbers, 2020)
    return a * b


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 866436


def test_test():
    assert run(read_input('test.txt')) == 514579
