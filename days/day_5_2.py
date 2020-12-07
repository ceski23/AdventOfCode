def run():
    with open('inputs/5.txt') as f:
        rows = [0 for _ in range(128)]
        cols = [0 for _ in range(8)]

        for line in f:
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

        my_row = rows.index(7)
        my_col = cols.index(105)
        seatID = (my_row * 8) + my_col
        return seatID


if __name__ == "__main__":
    print(run())
