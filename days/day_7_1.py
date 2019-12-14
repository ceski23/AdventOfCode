from itertools import permutations
from .utils.IntcodeComputer import IntcodeComputer
import asyncio

async def main():
  with open('inputs/7.txt') as f:
    memory = list(map(int, f.readline().split(',')))
    power = 0

    for phases in permutations(range(5)):
      inp = 0
      for phase in phases:
        computer = IntcodeComputer(memory.copy())
        await computer.start([phase, inp])
        inp = await computer.output.get()
        
      if (inp > power):
        power = inp
    
    print(power)

asyncio.run(main())