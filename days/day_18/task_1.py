from helpers import read_input
from operator import mul, add
import re

pattern = re.compile(r'[\d+\+\*\(\)]')


def parse_tasks(data):
    return [pattern.findall(line) for line in data]


def compute(data):
    numbers = []
    operators = []

    i = 0
    while i < len(data):
        if data[i] == '(':
            start = i+1
            end = start
            par = 0
            while data[end] != ')' or par != 0:
                if data[end] == '(':
                    par += 1
                elif data[end] == ')':
                    par -= 1
                end += 1
            numbers.append(compute(data[start:end]))
            i = end

        if data[i] == '+':
            operators.append(add)
        elif data[i] == '*':
            operators.append(mul)
        else:
            if len(operators) > 0:
                op = operators.pop()
                a = numbers.pop()
                b = int(data[i]) if len(numbers) == 0 else numbers.pop()
                numbers.append(op(a, b))
            elif data[i] != ')':
                numbers.append(int(data[i]))
        i += 1
    return numbers.pop()


def run(data):
    tasks = parse_tasks(data)
    return sum([compute(task) for task in tasks])


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 650217205854


def test_1():
    assert run(['1 + 2 * 3 + 4 * 5 + 6']) == 71


def test_2():
    assert run(['1 + (2 * 3) + (4 * (5 + 6))']) == 51


def test_3():
    assert run(['2 * 3 + (4 * 5)']) == 26


def test_4():
    assert run(['5 + (8 * 3 + 9 + 3 * 4 * 3)']) == 437


def test_5():
    assert run(['5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))']) == 12240


def test_6():
    assert run(['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2']) == 13632
