import numpy as np
from itertools import permutations
from asyncio import Queue, create_task, gather, run, sleep
from .utils.IntcodeComputer import IntcodeComputer

async def main():
  with open('inputs/7.txt') as f:
    memory = list(map(int, f.readline().split(',')))
    power = 0

    for phases in permutations(range(5, 10)):
      amps = []
      for phase in phases:
        amp = IntcodeComputer(memory.copy())
        amps.append(amp)

      tasks = []
      for i, phase in enumerate(phases):
        amps[i].inp = amps[i-1].output
        task = create_task(amps[i].start([phase]))
        tasks.append(task)
      
      await sleep(0)
      await amps[0].inp.put(0)
      await gather(*tasks)
      newPower = await amps[-1].output.get()

      if (newPower > power):
        power = newPower

    print(power)

run(main())