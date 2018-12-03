import re

def params(text):
  x = list(map(int, re.search(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', text).groups()))
  return {'id': x[0], 'x': x[1], 'y': x[2], 'w': x[3], 'h': x[4]}

result = 0
fabric = [[0 for x in range(1000)] for y in range(1000)]
lines = open('input.txt').read().splitlines()

for line in lines:
  p = params(line)
  for x in range(p['x'], p['x']+p['w']):
    for y in range(p['y'], p['y']+p['h']):
      if fabric[x][y] == 1: result += 1
      fabric[x][y] += 1

print(result)