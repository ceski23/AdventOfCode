from math import floor

def calcFuel(module):
  x = floor(module / 3) - 2
  return 0 if x <= 0 else x + calcFuel(x)

with open('inputs/1.txt') as f:
  inp = [int(x) for x in f]
  out = sum(map(calcFuel, inp))
  print(out)