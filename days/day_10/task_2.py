from task_1 import Code, check_syntax, get_opposite_bracket, is_opening, parse_input


def get_points(bracket: str):
    match bracket:
        case ')': return 1
        case ']': return 2
        case '}': return 3
        case '>': return 4
        case _: raise Exception('Invalid bracket')


def calc_autocomplete_points(code: Code):
    brackets: list[str] = []

    for char in code.source:
        if is_opening(char):
            brackets.append(char)
        else:
            brackets.pop()

    points = 0
    while len(brackets) > 0:
        bracket = get_opposite_bracket(brackets.pop())
        print(points)
        points = (points * 5) + get_points(bracket)

    return points


if __name__ == "__main__":
    lines_of_code = parse_input('test.txt')
    incomplete_lines = [
        line for line in lines_of_code if check_syntax(line) == True]
    points = sorted([calc_autocomplete_points(x) for x in incomplete_lines])
    print(points[int(len(points)/2)])
