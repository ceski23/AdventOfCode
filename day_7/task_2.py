import numpy as np
from itertools import permutations
from asyncio import Queue, create_task, gather, run, sleep

class IntcodeComputer:
  def __init__(self, memory, i):
    self.memory = memory
    self.pointer = 0
    self.output = Queue()
    self.inp = Queue()
    self.i = i
  
  def parseArg(self, mode, value):
    return {
      '0': lambda: self.memory[value],
      '1': lambda: value,
    }[mode]()
  
  def parseDest(self, mode, value):
    return {
      '0': lambda: value,
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

  def getOperation(self, opcode):
    return {
      1: (self.add, 3),
      2: (self.multiply, 3),
      3: (self.read, 1),
      4: (self.write, 1),
      5: (self.jumpTrue, 2),
      6: (self.jumpFalse, 2),
      7: (self.ifLess, 3),
      8: (self.ifEquals, 3)
    }.get(opcode, (self.halt, 0))

  async def start(self, inp):
    for a in inp[::-1]:
      self.inp.put_nowait(a)

    while (0 <= self.pointer < len(self.memory)):
      command = str(self.memory[self.pointer])
      opcode = int(command[-2:])
      operation, argCount = self.getOperation(opcode)
      modes = command[:-2].zfill(argCount)[::-1]
      await operation(modes)

async def main():
  with open('input.txt') as f:
    memory = list(map(int, f.readline().split(',')))
    power = 0

    for phases in permutations(range(5, 10)):
      amps = []
      for i, phase in enumerate(phases):
        amp = IntcodeComputer(memory.copy(), i)
        amps.append(amp)

      tasks = []
      for i, phase in enumerate(phases):
        amps[i].inp = amps[i-1].output
        task = create_task(amps[i].start([phase]))
        tasks.append(task)
      
      await sleep(0)
      await amps[0].inp.put(0)
      await gather(*tasks, return_exceptions=True)
      newPower = await amps[-1].output.get()

      if (newPower > power):
        power = newPower

    print(power)

run(main())