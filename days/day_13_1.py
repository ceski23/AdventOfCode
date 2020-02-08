import numpy as np
from asyncio import Queue, create_task, gather, run, sleep
from .utils.IntcodeComputer import IntcodeComputer

async def main():
  with open('inputs/13.txt') as f:
    code = list(map(int, f.readline().split(',')))
    game = IntcodeComputer(code.copy())
    tilesCount = {}

    await game.start([])

    while not game.output.empty():
      x = await game.output.get()
      y = await game.output.get()
      tileId = await game.output.get()

      tilesCount[tileId] = tilesCount.get(tileId, 0) + 1
      
    print(tilesCount)
    
run(main())