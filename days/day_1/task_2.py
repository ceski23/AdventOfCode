from task_1 import parse_input


def sliding_window(list: list[int], size: int):
  return (list[i: i + size] for i in range(len(list) - size + 1))


def count_sliding_depth_increases(report: list[int]):
  count = 0
  prev_depth = -1
  for depths in sliding_window(report, 3):
    depth = sum(depths)
    if prev_depth != -1 and depth > prev_depth:
      count += 1
    prev_depth = depth
  return count


if __name__ == "__main__":
  report = parse_input('input.txt')
  count = count_sliding_depth_increases(report)
  print(count)
