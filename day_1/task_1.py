from math import floor

def calcFuel(module):
  return floor(module / 3) - 2

with open('input.txt') as f:
  inp = [int(x) for x in f]
  out = sum(map(calcFuel, inp))
  print(out)