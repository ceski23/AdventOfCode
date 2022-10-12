from task_1 import parse_input, run_bingo


if __name__ == "__main__":
    numbers, boards = parse_input('input.txt')
    score = [score for score in run_bingo(numbers, boards)][-1]
    print(score)
