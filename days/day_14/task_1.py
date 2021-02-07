from helpers import read_input
import re

mask_pattern = re.compile(r'^mask = ([X01]+)$')
operation_pattern = re.compile(r'^mem\[(\d+)\] = (\d+)$')


class Memory:
    def __init__(self):
        self.mem = {}
        self.mask = '0' * 36

    def __setitem__(self, key, value):
        output = ''
        bin_value = format(value, '036b')
        for m, v in zip(self.mask, bin_value):
            output += v if m == 'X' else m
        self.mem[key] = int(output, 2)


def run(data):
    mem = Memory()
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
    assert run(read_input('input.txt')) == 8332632930672


def test_1():
    assert run(read_input('test_1.txt')) == 165
