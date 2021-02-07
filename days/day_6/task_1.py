from helpers import read_input


def countGroup(group):
    yes = set()
    for questions in group:
        for question in questions:
            if question not in yes:
                yes.add(question)
    return len(yes)


def run(data):
    group = []
    count = 0
    for line in data:
        if len(line.strip()) > 0:
            group.append(line.strip())
        else:
            count += countGroup(group)
            group = []
    count += countGroup(group)
    return count


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 6443


def test_1():
    assert run(read_input('test_1.txt')) == 6


def test_2():
    assert run(read_input('test_2.txt')) == 11
