import numpy as np
from asyncio import Queue, create_task, gather, run
from .utils.IntcodeComputer import IntcodeComputer

async def main():
  with open('inputs/11.txt') as f:
    code = list(map(int, f.readline().split(',')))

    pos, direction = (0, 0), 0
    hull = {}
    robot = IntcodeComputer(code.copy())
    task = create_task(robot.start([]))

    while (0 <= robot.pointer < len(robot.memory)):
      await robot.inp.put(hull.get(pos, 0))
      
      hull[pos] = await robot.output.get()
      turnDirection = 1 if await robot.output.get() else -1

      direction = (direction + turnDirection) % 4

      pos = {
        0: (pos[0], pos[1] + 1),
        1: (pos[0] + 1, pos[1]),
        2: (pos[0], pos[1] - 1),
        3: (pos[0] - 1, pos[1])
      }[direction]

    await gather(task)
    print(len(hull))

run(main())