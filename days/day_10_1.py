import numpy as np

def przekatna(asteroidsMap, x, y, poziom, pion):
  for i in range(1, asteroidsMap.shape[1] - x + 2):
    for j in range(1, asteroidsMap.shape[0] - y + 2):
      k, found = 1, False
      while (
        0 <= (ny := y + k * j * pion) < asteroidsMap.shape[0] and
        0 <= (nx := x + k * i * poziom) < asteroidsMap.shape[1]
      ):
        if (asteroidsMap[ny, nx] == '#'):
          if found: asteroidsMap[ny, nx] = '@'
          else: found = True
        k += 1

def prosta(asteroidsMap, x, y, axis, step):
  k, found = step, False
  while (0 <= (n := x + k if axis == 1 else y + k) < asteroidsMap.shape[axis]):
    if (asteroidsMap[y if axis == 1 else n, x if axis == 0 else n] == '#'):
      if found: asteroidsMap[y if axis == 1 else n, x if axis == 0 else n] = '@'
      else: found = True
    k += step

with open('inputs/10.txt') as f:
  data = [list(line) for line in f.read().splitlines()]
  asteroids = [(y, x) for y, x in zip(*np.where(np.array(data) == '#'))]
  
  maxa, pos = 0, None
  for y, x in asteroids:
    asteroidsMap = np.array(data)
    asteroidsMap[y, x] = 'O'

    prosta(asteroidsMap, x, y, 1, +1) # Dół
    prosta(asteroidsMap, x, y, 1, -1) # Góra
    prosta(asteroidsMap, x, y, 0, +1) # Prawo
    prosta(asteroidsMap, x, y, 0, -1) # Lewo
    
    przekatna(asteroidsMap, x, y, +1, +1) # Dół prawo
    przekatna(asteroidsMap, x, y, -1, +1) # Dół lewo
    przekatna(asteroidsMap, x, y, +1, -1) # Góra prawo
    przekatna(asteroidsMap, x, y, -1, -1) # Góra lewo

    if (visible := np.sum(asteroidsMap == '#')) > maxa:
      maxa = visible
      pos = (x, y)

  print(maxa, pos)