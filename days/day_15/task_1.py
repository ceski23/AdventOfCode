from helpers import read_input


def nth_spoken_number(numbers, n):
    spoken = {}
    for i, number in enumerate(numbers):
        spoken[number] = [i+1]

    last = numbers[-1]
    for i in range(len(numbers)+1, n+1):
        if len(spoken.get(last, [])) < 2:  # nowy
            last = 0
        else:
            last = spoken[last][-1] - spoken[last][-2]

        if last not in spoken:
            spoken[last] = []
        spoken[last].append(i)
    return last


def run(data):
    numbers = [int(n) for n in data[0].split(',')]
    return nth_spoken_number(numbers, 2020)


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 758


def test_1():
    assert run(read_input('test_1.txt')) == 436


def test_2():
    assert run(read_input('test_2.txt')) == 1


def test_3():
    assert run(read_input('test_3.txt')) == 10


def test_4():
    assert run(read_input('test_4.txt')) == 27


def test_5():
    assert run(read_input('test_5.txt')) == 78


def test_6():
    assert run(read_input('test_6.txt')) == 438


def test_7():
    assert run(read_input('test_7.txt')) == 1836
