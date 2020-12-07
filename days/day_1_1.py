def findTwo(numbers, x):
    diffs = {}

    for number in numbers:
        if diffs.get(number):
            return [number, diffs.get(number)]
        diffs[x - number] = number


def run():
    with open('inputs/1.txt') as f:
        lines = f.readlines()
        numbers = [int(x) for x in lines]
        a, b = findTwo(numbers, 2020)
        return a * b


if __name__ == "__main__":
    print(run())
