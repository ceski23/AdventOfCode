from pathlib import Path
import os
from dataclasses import dataclass
import numpy as np
import numpy.typing as npt


@dataclass
class BingoBoard:
    numbers: npt.NDArray[np.int64]

    def calc_score(self, last_number: int) -> int:
        return np.sum(self.numbers) * last_number  # type: ignore

    def check_bingo(self):
        for row in range(self.numbers.shape[0]):
            sum = self.numbers[row, :].sum()
            if sum == 0:
                return True
        for column in range(self.numbers.shape[1]):
            sum = self.numbers[:, column].sum()
            if sum == 0:
                return True
        return False

    def mark_number(self, num: int):
        indices: npt.NDArray[np.int64] = np.where(  # type: ignore
            self.numbers == num)  # type: ignore
        self.numbers[indices] = 0
        return self.check_bingo()


def parse_input(path: str):
    with Path(os.path.dirname(__file__), path).open() as f:
        draw_numbers = [int(n) for n in f.readline().strip().split(',')]
        boards: list[BingoBoard] = []
        tmp: list[list[int]] = []

        f.readline()

        for line in f:
            match line:
                case '\n':
                    board = BingoBoard(np.array(tmp.copy()))  # type: ignore
                    boards.append(board)
                    tmp.clear()
                case l:
                    row = [int(n) for n in l.split()]
                    tmp.append(row)

        board = BingoBoard(np.array(tmp.copy()))  # type: ignore
        boards.append(board)
        tmp.clear()
    return (draw_numbers, boards)


def run_bingo(numbers: list[int], boards: list[BingoBoard]):
    for number in numbers:
        results = [board.mark_number(number) for board in boards]
        for i, bingo in enumerate(results):
            if bingo:
                yield boards[i].calc_score(number)
        boards = [board for i, board in enumerate(
            boards) if results[i] == False]


if __name__ == "__main__":
    numbers, boards = parse_input('test.txt')
    score = next(run_bingo(numbers, boards))
    print(score)
