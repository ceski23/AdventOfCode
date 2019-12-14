import numpy as np
from asyncio import Queue, create_task, gather, run, sleep

class IntcodeComputer:
  def __init__(self, program):
    self.memory = [0 for _ in range(64 * 1024)]
    self.memory[:len(program)] = program
    self.pointer = 0
    self.output = Queue()
    self.inp = Queue()
    self.relativeBase = 0
  
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

  async def add(self, modes):
    a, b = self.readArgs(modes, 2)
    dest = self.parseDest(modes[2], self.memory[self.pointer+3])
    self.memory[dest] = a + b
    self.pointer += 3 + 1

  async def multiply(self, modes):
    a, b = self.readArgs(modes, 2)
    dest = self.parseDest(modes[2], self.memory[self.pointer+3])
    self.memory[dest] = a * b
    self.pointer += 3 + 1

  async def read(self, modes):
    val = await self.inp.get()
    dest = self.parseDest(modes[0], self.memory[self.pointer+1])
    self.memory[dest] = val
    self.pointer += 1 + 1
    self.inp.task_done()

  async def write(self, modes):
    a, = self.readArgs(modes, 1)
    await self.output.put(a)
    self.pointer += 1 + 1

  async def halt(self, *args):
    self.pointer = -1

  async def jumpTrue(self, modes):
    a, b = self.readArgs(modes, 2)
    self.pointer = b if a != 0 else self.pointer + 2 + 1

  async def jumpFalse(self, modes):
    a, b = self.readArgs(modes, 2)
    self.pointer = b if a == 0 else self.pointer + 2 + 1

  async def ifLess(self, modes):
    a, b = self.readArgs(modes, 2)
    dest = self.parseDest(modes[2], self.memory[self.pointer+3])
    self.memory[dest] = 1 if a < b else 0
    self.pointer += 3 + 1

  async def ifEquals(self, modes):
    a, b = self.readArgs(modes, 2)
    dest = self.parseDest(modes[2], self.memory[self.pointer+3])
    self.memory[dest] = 1 if a == b else 0
    self.pointer += 3 + 1
  
  async def changeRelativeBase(self, modes):
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

  async def start(self, inp):
    try:
      for a in inp:
        self.inp.put_nowait(a)

      while (0 <= self.pointer < len(self.memory)):
        command = str(self.memory[self.pointer])
        opcode = int(command[-2:])
        operation, argCount = self.getOperation(opcode)
        modes = command[:-2].zfill(argCount)[::-1]
        await operation(modes)
    except Exception as e:
      print(e)