from task_1 import parse_input, Submarine, calculate_position


class BetterSubmarine(Submarine):
  aim = 0

  def forward(self, units: int):
    self.horizontal_position += units
    self.depth += self.aim * units

  def up(self, units: int):
    self.aim -= units

  def down(self, units: int):
    self.aim += units


if __name__ == "__main__":
  instructions = parse_input('input.txt')
  submarine = BetterSubmarine()
  position = calculate_position(submarine, instructions)
  print(position)
