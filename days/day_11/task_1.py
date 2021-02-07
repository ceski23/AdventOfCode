from helpers import read_input


def count_adjacent(layout, i, j):
    count = 0
    if i > 0:
        # góra-lewo
        if j > 0 and layout[i-1][j-1] == '#':
            count += 1
        # góra
        if layout[i-1][j] == '#':
            count += 1
        # góra-prawo
        if j < len(layout[i-1])-1 and layout[i-1][j+1] == '#':
            count += 1

    if j > 0:
        # lewo
        if layout[i][j-1] == '#':
            count += 1

    if j < len(layout[i])-1:
        # prawo
        if layout[i][j+1] == '#':
            count += 1

    if i < len(layout)-1:
        # dół-lewo
        if j > 0 and layout[i+1][j-1] == '#':
            count += 1
        # dół
        if layout[i+1][j] == '#':
            count += 1
        # dół-prawo
        if j < len(layout[i+1])-1 and layout[i+1][j+1] == '#':
            count += 1
    return count


def simulate(layout):
    changes = []
    occupied = 0
    for i, row in enumerate(layout):
        for j, seat in enumerate(row):
            adjacent = count_adjacent(layout, i, j)
            if seat == 'L' and adjacent == 0:
                changes.append((i, j, '#'))
            elif seat == '#' and adjacent >= 4:
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
    assert run(read_input('input.txt')) == 2273


def test_test():
    assert run(read_input('test.txt')) == 37
