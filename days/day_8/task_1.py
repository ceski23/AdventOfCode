from helpers import read_input


class Console:
    def __init__(self, code):
        self.acc = 0
        self.pointer = 0
        self.code = code

    def process(self, operation, arg):
        if operation == 'acc':
            self.acc += arg
            self.pointer += 1
        elif operation == 'nop':
            self.pointer += 1
        elif operation == 'jmp':
            self.pointer += arg


def find_loop(code):
    console = Console(code)
    visited = set()
    while console.pointer not in visited:
        if console.pointer >= len(code):
            return (False, console.acc)
        visited.add(console.pointer)
        op, arg = console.code[console.pointer]
        console.process(op, arg)
    return (True, console.acc)


def run(data):
    boot_code = []
    for line in data:
        operation, arg = line.strip().split(' ')
        boot_code.append((operation, int(arg)))

    return find_loop(boot_code)[1]


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 1489


def test_test():
    assert run(read_input('test.txt')) == 5
