from helpers import read_input
from operator import mul, add
import re
from days.day_18.task_1 import compute, parse_tasks


def add_parentheses(orig_task):
    task = orig_task.copy()
    i = 0
    parentheses = 0

    while i < len(task):
        if task[i] == '(':
            parentheses += 1

        elif task[i] == ')':
            parentheses -= 1

        elif task[i] == '*':
            task.insert(i+1, '(')

            if parentheses == 0:
                task.append(')')
                parentheses += 1
            else:
                orig_par = parentheses
                parentheses += 1

                pos = i
                while parentheses != orig_par and pos < len(task):
                    if task[pos] == '(':
                        parentheses += 1
                    if task[pos] == ')':
                        parentheses -= 1
                    pos += 1
                task.insert(pos, ')')
        i += 1
    return task


def run(data):
    tasks = parse_tasks(data)
    fixed_tasks = [add_parentheses(task) for task in tasks]
    return sum([compute(task) for task in fixed_tasks])


if __name__ == "__main__":
    print(run(
        ['3 * 2 * 7 + 4 * 5 * ((2 + 9 * 5) + 8 + 4 + 5 * (5 + 3 + 6 + 4 + 8 * 4) + 4)']))
    # print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == False


def test_1():
    assert run(['1 + 2 * 3 + 4 * 5 + 6']) == 231


def test_2():
    assert run(['1 + (2 * 3) + (4 * (5 + 6))']) == 51


def test_3():
    assert run(['2 * 3 + (4 * 5)']) == 46


def test_4():
    assert run(['5 + (8 * 3 + 9 + 3 * 4 * 3)']) == 1445


def test_5():
    assert run(['5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))']) == 669060


def test_6():
    assert run(['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2']) == 23340
