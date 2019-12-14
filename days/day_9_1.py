import asyncio
from .utils.IntcodeComputer import IntcodeComputer

async def main():
  with open('inputs/9.txt') as f:
    code = list(map(int, f.readline().split(',')))
    computer = IntcodeComputer(code)
    await computer.start([1])
    print(await computer.output.get())

asyncio.run(main())