def run():
    with open('inputs/5.txt') as f:
        highestID = 0

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

            seatID = (min_row * 8) + min_col
            if seatID > highestID:
                highestID = seatID

        return highestID


if __name__ == "__main__":
    print(run())
