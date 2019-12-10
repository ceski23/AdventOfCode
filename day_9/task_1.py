class IntcodeComputer:
  def __init__(self, memory):
    self.memory = memory
    self.pointer = 0
    self.output = []
    self.inp = []
    self.relativeBase = 0

  def writeToMemory(self, where, what):
    self.memory[where] = what
  
  def parseArg(self, mode, value):
    return {
      '0': lambda: self.memory[value],
      '1': lambda: value,
      '2': lambda: self.memory[self.relativeBase + value]
    }[mode]()
  
  def parseDest(self, mode, value):
    return {
      '0': lambda: value,
      '2': lambda: self.relativeBase + value
    }[mode]()
  
  def readArgs(self, modes, n):
    args = self.memory[self.pointer + 1 : self.pointer + 1 + n]
    return [self.parseArg(modes[i], args[i]) for i in range(n)]

  def add(self, modes):
    a, b = self.readArgs(modes, 2)
    dest = self.parseDest(modes[2], self.memory[self.pointer+3])
    self.memory[dest] = a + b
    self.pointer += 3 + 1

  def multiply(self, modes):
    a, b = self.readArgs(modes, 2)
    dest = self.parseDest(modes[2], self.memory[self.pointer+3])
    self.memory[dest] = a * b
    self.pointer += 3 + 1

  def read(self, modes):
    val = self.inp.pop()
    dest = self.parseDest(modes[0], self.memory[self.pointer+1])
    self.memory[dest] = val
    self.pointer += 1 + 1

  def write(self, modes):
    a, = self.readArgs(modes, 1)
    self.output.append(a)
    self.pointer += 1 + 1

  def halt(self, *args):
    self.pointer = -1

  def jumpTrue(self, modes):
    a, b = self.readArgs(modes, 2)
    self.pointer = b if a != 0 else self.pointer + 2 + 1

  def jumpFalse(self, modes):
    a, b = self.readArgs(modes, 2)
    self.pointer = b if a == 0 else self.pointer + 2 + 1

  def ifLess(self, modes):
    a, b = self.readArgs(modes, 2)
    dest = self.parseDest(modes[2], self.memory[self.pointer+3])
    self.memory[dest] = 1 if a < b else 0
    self.pointer += 3 + 1

  def ifEquals(self, modes):
    a, b = self.readArgs(modes, 2)
    dest = self.parseDest(modes[2], self.memory[self.pointer+3])
    self.memory[dest] = 1 if a == b else 0
    self.pointer += 3 + 1
  
  def changeRelativeBase(self, modes):
    a, = self.readArgs(modes, 1)
    self.relativeBase += a
    self.pointer += 1 + 1

  def getOperation(self, opcode):
    return {
      1: (self.add, 3),
      2: (self.multiply, 3),
      3: (self.read, 1),
      4: (self.write, 1),
      5: (self.jumpTrue, 2),
      6: (self.jumpFalse, 2),
      7: (self.ifLess, 3),
      8: (self.ifEquals, 3),
      9: (self.changeRelativeBase, 1),
    }.get(opcode, (self.halt, 0))

  def start(self, inp):
    self.inp = inp[::-1]

    while (0 <= self.pointer < len(self.memory)):
      command = str(self.memory[self.pointer])
      opcode = int(command[-2:])
      operation, argCount = self.getOperation(opcode)
      modes = command[:-2].zfill(argCount)[::-1]
      operation(modes)
    return self.output

with open('input.txt') as f:
  memory = [0 for _ in range(64 * 1024)]

  code = list(map(int, f.readline().split(',')))
  memory[:len(code)] = code

  computer = IntcodeComputer(memory)
  print(computer.start([1]))