import numpy as np
from asyncio import Queue, create_task, gather, run, sleep
from .utils.IntcodeComputer import IntcodeComputer

def drawMap(tiles):
  minX, minY = 0, 0
  maxX, maxY = 0, 0
  for x, y in tiles:
    if x < minX: minX = x
    if y < minY: minY = y
    if x > maxX: maxX = x
    if y > maxY: maxY = y
  
  print((minX, minY), (maxX, maxY))
  
  plate = np.zeros((maxY - minY + 1, maxX - minX + 1))
  for x, y in tiles:
    plate[y + abs(minY), x + abs(minX)] = tiles[(x, y)]
  
  for line in plate:
    for x in map(str, map(int, line.tolist())):
      if x == '4': print('O', end='')
      elif x != '0': print('#', end='')
      else: print(' ', end='')
    print()

async def main():
  with open('inputs/13.txt') as f:
    code = list(map(int, f.readline().split(',')))
    game = IntcodeComputer(code.copy())
    score = 0
    tiles = {}

    game.memory[0] = 2

    task = create_task(game.start([]))
    await sleep(0)

    while (0 <= game.pointer < len(game.memory)):
      await sleep(1)
      tiles = {}
      while not game.output.empty():
        x = await game.output.get()
        y = await game.output.get()
        data = await game.output.get()

        print(x, y, ' | ', data)

        if (x == -1 and y == 0):
          print('SCORE:', data)
          score = data
        else:
          if data != 0:
            tiles[(x, y)] = data
      
      drawMap(tiles)

      if game.inp.empty():
        joy = int(input('Podaj joystick:'))
        await game.inp.put(joy)
        
    await gather(task)
    
run(main())