from helpers import read_input
from days.day_1.task_1 import findTwo


def find_contiguous(numbers, invalid):
    for i in range(len(numbers)-1, 0, -1):
        if numbers[i] < invalid:
            contiguous, suma = [numbers[i]], numbers[i]
            for j in range(i-1, 0, -1):
                if numbers[j] >= invalid:
                    continue
                contiguous.append(numbers[j])
                suma += numbers[j]
                if suma == invalid:
                    return contiguous
                elif suma > invalid:
                    break


def run(data, preamble_size):
    numbers = []
    invalid = None
    for line in data:
        number = int(line)
        if len(numbers) > preamble_size and not findTwo(numbers[-preamble_size:], number):
            invalid = number
        numbers.append(number)
    n = sorted(find_contiguous(numbers, invalid))
    return n[0] + n[-1]


if __name__ == "__main__":
    print(run(read_input('input.txt'), 25))


def test_input():
    assert run(read_input('input.txt'), 25) == 96081673


def test_test():
    assert run(read_input('test.txt'), 5) == 62
