from helpers import read_input
from days.day_8.task_1 import find_loop


def run(data):
    boot_code, acc = [], 0
    ops = []
    for line in data:
        operation, arg = line.strip().split(' ')
        boot_code.append((operation, int(arg)))
        if operation in ['jmp', 'nop']:
            ops.append(len(boot_code)-1)

    for i in ops:
        x = boot_code.copy()
        op, arg = x[i]
        x[i] = ('nop', arg) if op == 'jmp' else ('jmp', arg)

        is_loop, acc = find_loop(x)
        if not is_loop:
            return acc


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 1539


def test_test():
    assert run(read_input('test.txt')) == 8
