import re

def params(text):
  x = list(map(int, re.search(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', text).groups()))
  return {'id': x[0], 'x': x[1], 'y': x[2], 'w': x[3], 'h': x[4]}

result = 0
seen = dict()
lines = open('input.txt').read().splitlines()

for line in lines:
  p = params(line)
  for x in range(p['x'], p['x']+p['w']):
    for y in range(p['y'], p['y']+p['h']):
      n = y * 1000 + x
      if (n in seen):
        if (seen[n] == 1): result += 1
        seen[n] += 1
      else:
        seen[n] = 1

print(result)