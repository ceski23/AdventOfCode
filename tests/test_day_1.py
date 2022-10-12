from days.day_1.task_1 import parse_input, count_depth_increases
from days.day_1.task_2 import count_sliding_depth_increases


def test_task_1_test():
  report = parse_input('test.txt')
  assert count_depth_increases(report) == 7


def test_task_1_input():
  report = parse_input('input.txt')
  assert count_depth_increases(report) == 1581


def test_task_2_test():
  report = parse_input('test.txt')
  assert count_sliding_depth_increases(report) == 5


def test_task_2_input():
  report = parse_input('input.txt')
  assert count_sliding_depth_increases(report) == 1618
