import numpy as np
from asyncio import Queue, create_task, gather, run, sleep
from .utils.IntcodeComputer import IntcodeComputer

async def main():
  with open('inputs/11.txt') as f:
    memory = [0 for _ in range(64 * 1024)]
    code = list(map(int, f.readline().split(',')))
    memory[:len(code)] = code

    pos, direction = (0, 0), 0
    hull = {pos: 1}
    robot = IntcodeComputer(memory.copy())
    task = create_task(robot.start([]))

    while (0 <= robot.pointer < len(memory)):
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

    minX, minY = 0, 0
    maxX, maxY = 0, 0
    for x, y in hull:
      if x < minX: minX = x
      if y < minY: minY = y
      if x > maxX: maxX = x
      if y > maxY: maxY = y
    
    plate = np.full((maxY - minY + 1, maxX - minX + 1), 2)
    for x, y in hull:
      plate[y + abs(minY), x + abs(minX)] = hull[(x, y)]
    
    for line in plate[::-1]:
      for x in map(str, line.tolist()):
        print('1' if x == '1' else ' ', end='')
      print()
    
run(main())