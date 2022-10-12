from days.day_2.task_1 import parse_input, Submarine, calculate_position
from days.day_2.task_2 import BetterSubmarine


def test_task_1_test():
  instructions = parse_input('test.txt')
  submarine = Submarine()
  assert calculate_position(submarine, instructions) == 150


def test_task_1_input():
  instructions = parse_input('input.txt')
  submarine = Submarine()
  assert calculate_position(submarine, instructions) == 1990000


def test_task_2_test():
  instructions = parse_input('test.txt')
  submarine = BetterSubmarine()
  assert calculate_position(submarine, instructions) == 900


def test_task_2_input():
  instructions = parse_input('input.txt')
  submarine = BetterSubmarine()
  assert calculate_position(submarine, instructions) == 1975421260
