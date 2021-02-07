from helpers import read_input


def findThree(numbers, x):
    diffs = {}

    for number in numbers:
        diffs[x - number] = number

    diffs2 = {}
    for rest, n in diffs.items():
        for number in numbers:
            if diffs2.get(number):
                return [number, diffs2.get(number), n]
            diffs2[rest - number] = number


def run(data):
    numbers = [int(x) for x in data]
    a, b, c = findThree(numbers, 2020)
    return a * b * c


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 276650720


def test_test():
    assert run(read_input('test.txt')) == 241861950
