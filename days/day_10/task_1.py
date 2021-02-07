from helpers import read_input


def select(adapters, ratings):
    if len(adapters) > 0:
        last = ratings[-1]
        good = list(filter(lambda x: last < x <= last+3, adapters))

        for adapter in good:
            new_adapters = adapters.copy()
            new_adapters.pop(adapters.index(adapter))
            results = select(new_adapters, [*ratings, adapter])
            if results:
                return results
    else:
        return ratings


def run(data):
    adapters = sorted([int(x) for x in data])
    built_in = adapters[-1] + 3

    select_adapters = select(adapters, [0])
    select_adapters.append(built_in)

    diffs = {}
    for a, b in zip(select_adapters[:-1], select_adapters[1:]):
        diff = b - a
        if diff not in diffs:
            diffs[diff] = 1
        else:
            diffs[diff] += 1

    return diffs[1] * diffs[3]


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 2310


def test_1():
    assert run(read_input('test_1.txt')) == 35


def test_2():
    assert run(read_input('test_2.txt')) == 220
