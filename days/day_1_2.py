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


def run():
    with open('inputs/1.txt') as f:
        lines = f.readlines()
        numbers = [int(x) for x in lines]
        a, b, c = findThree(numbers, 2020)
        return a * b * c


if __name__ == "__main__":
    print(run())
