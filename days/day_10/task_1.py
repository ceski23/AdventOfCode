from pathlib import Path
import os
from dataclasses import dataclass


def is_opening(bracket: str):
    match bracket:
        case '(' | '[' | '{' | '<': return True
        case _: return False


def get_opposite_bracket(bracket: str):
    match bracket:
        case '(': return ')'
        case '[': return ']'
        case '{': return '}'
        case '<': return '>'
        case ')': return '('
        case ']': return '['
        case '}': return '{'
        case '>': return '<'
        case _: raise Exception('Invalid bracket')


def get_points(bracket: str):
    match bracket:
        case ')': return 3
        case ']': return 57
        case '}': return 1197
        case '>': return 25137
        case _: raise Exception('Invalid bracket')


@dataclass
class Code:
    source: str


def parse_input(path: str):
    with Path(os.path.dirname(__file__), path).open() as f:
        return [Code(line.strip()) for line in f]


def check_syntax(code: Code):
    brackets: list[str] = []

    for char in code.source:
        if (is_opening(char)):
            brackets.append(char)
        else:
            expected_bracket = brackets.pop()
            opening_bracket = get_opposite_bracket(char)
            if expected_bracket != opening_bracket:
                return char
    return True


if __name__ == "__main__":
    lines_of_code = parse_input('input.txt')
    points = 0
    for line in lines_of_code:
        if (bracket := check_syntax(line)) != True:
            points += get_points(bracket)
    print(points)
