from helpers import read_input


def run(data):
    rows = [0 for _ in range(128)]
    cols = [0 for _ in range(8)]

    for line in data:
        min_row, max_row = 0, 127
        min_col, max_col = 0, 7
        code = line.strip()

        for i in range(7):
            if code[i] == 'F':
                max_row -= pow(2, 6-i)
            elif code[i] == 'B':
                min_row += pow(2, 6-i)

        for i in range(3):
            if code[i+7] == 'L':
                max_col -= pow(2, 2-i)
            elif code[i+7] == 'R':
                min_col += pow(2, 2-i)

        rows[min_row] += 1
        cols[min_col] += 1

    my_row = rows.index(next(filter(lambda row: 8 > row > 0, rows)))
    my_col = cols.index(min(cols))
    seatID = (my_row * 8) + my_col
    return seatID


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 657
