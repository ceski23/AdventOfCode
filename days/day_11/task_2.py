from helpers import read_input


def left(layout, i, j):
    return range(j-1, -1, -1)


def top(layout, i, j):
    return range(i-1, -1, -1)


def right(layout, i, j):
    return range(j+1, len(layout[i]), 1)


def bottom(layout, i, j):
    return range(i+1, len(layout), 1)


def count(layout, i, j):
    count = 0
    params = (layout, i, j)
    coords = [
        zip(top(*params), left(*params)),
        zip(top(*params), [j for _ in top(*params)]),
        zip(top(*params), right(*params)),
        zip([i for _ in left(*params)], left(*params)),
        zip([i for _ in right(*params)], right(*params)),
        zip(bottom(*params), left(*params)),
        zip(bottom(*params), [j for _ in bottom(*params)]),
        zip(bottom(*params), right(*params))
    ]
    for c in coords:
        for i, j in c:
            if layout[i][j] == '#':
                count += 1
                break
            if layout[i][j] == 'L':
                break
    return count


def simulate(layout):
    changes = []
    occupied = 0
    for i, row in enumerate(layout):
        for j, seat in enumerate(row):
            if seat == '.':
                continue
            adjacent = count(layout, i, j)
            if seat == 'L' and adjacent == 0:
                changes.append((i, j, '#'))
            elif seat == '#' and adjacent >= 5:
                changes.append((i, j, 'L'))
    for i, j, seat in changes:
        layout[i][j] = seat
    return layout, len(changes)


def run(data):
    seat_layout = [list(x) for x in data]

    while True:
        seat_layout, changes_count = simulate(seat_layout)

        if changes_count == 0:
            occupied = 0
            for row in seat_layout:
                for seat in row:
                    if seat == '#':
                        occupied += 1
            return occupied


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 2064


def test_test():
    assert run(read_input('test.txt')) == 26
