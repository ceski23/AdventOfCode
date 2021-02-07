from helpers import read_input
from days.day_14.task_1 import Memory, mask_pattern, operation_pattern
import itertools


class MemoryV2(Memory):
    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        output = ''
        bin_key = format(key, '036b')
        for m, k in zip(self.mask, bin_key):
            output += m if m == 'X' else k if m == '0' else m

        floatings = [i for i, x in enumerate(output) if x == 'X']

        for replacements in itertools.product(range(2), repeat=len(floatings)):
            address = list(output)
            for idx_to_replace, replacement in zip(floatings, replacements):
                address[idx_to_replace] = str(replacement)
            self.mem[int(''.join(address), 2)] = value


def run(data):
    mem = MemoryV2()
    for line in data:
        if match := mask_pattern.search(line):
            mem.mask = match.group(1)
        elif match := operation_pattern.search(line):
            address = int(match.group(1))
            value = int(match.group(2))
            mem[address] = value
    return sum(mem.mem.values())


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 4753238784664


def test_2():
    assert run(read_input('test_2.txt')) == 208
