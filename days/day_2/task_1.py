from dataclasses import dataclass
from pathlib import Path
import os
from enum import Enum, auto


class Direction(Enum):
  UP = auto()
  DOWN = auto()
  FORWARD = auto()

  @staticmethod
  def from_string(direction: str):
    match direction:
      case 'forward': return Direction.FORWARD
      case 'up': return Direction.UP
      case 'down': return Direction.DOWN
      case _: raise TypeError('Invalid direction')


class Submarine:
  horizontal_position = 0
  depth = 0

  def forward(self, units: int):
    self.horizontal_position += units

  def up(self, units: int):
    self.depth -= units

  def down(self, units: int):
    self.depth += units

  def move(self, direction: Direction, units: int):
    match direction:
      case Direction.FORWARD: self.forward(units)
      case Direction.DOWN: self.down(units)
      case Direction.UP: self.up(units)
      case _: raise TypeError('Invalid direction')


@dataclass
class Instruction:
  direction: Direction
  units: int


def parse_input(path: str):
  with Path(os.path.dirname(__file__), path).open() as f:
    input: list[Instruction] = []
    for line in f:
      splitted = line.split(' ')
      input.append(Instruction(
          Direction.from_string(splitted[0]), int(splitted[1])))
    return input


def calculate_position(submarine: Submarine, instructions: list[Instruction]):
  for ins in instructions:
    submarine.move(ins.direction, ins.units)
  return submarine.depth * submarine.horizontal_position


if __name__ == "__main__":
  instructions = parse_input('input.txt')
  submarine = Submarine()
  position = calculate_position(submarine, instructions)
  print(position)
