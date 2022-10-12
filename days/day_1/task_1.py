from pathlib import Path
import os


def parse_input(path: str):
  with Path(os.path.dirname(__file__), path).open() as f:
    return [int(line) for line in f]


def count_depth_increases(report: list[int]):
  count = 0
  prev_depth = -1
  for depth in report:
    if prev_depth != -1 and depth > prev_depth:
      count += 1
    prev_depth = depth
  return count


if __name__ == "__main__":
  report = parse_input('input.txt')
  count = count_depth_increases(report)
  print(count)
