import re
from itertools import combinations
import copy
from time import time

with open('inputs/12.txt') as f:
  s = time()
  moonsPos, zero = [], []
  for line in f:
    match = re.match(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line)
    pos = list(map(int, match.groups()))
    moonsPos.append(pos)
    zero.append([0, 0, 0])
  
  moonsVel = copy.deepcopy(zero)

  for n in range(100000):
    velDelta = copy.deepcopy(zero)

    for i, j in combinations(range(len(moonsPos)), 2):
      for k in range(3):
        if moonsPos[i][k] < moonsPos[j][k]:
          velDelta[i][k] += 1
          velDelta[j][k] += -1
        elif moonsPos[i][k] > moonsPos[j][k]:
          velDelta[i][k] += -1
          velDelta[j][k] += 1
    
    for i in range(len(moonsPos)):
      for j in range(3):
        moonsVel[i][j] += velDelta[i][j]
        moonsPos[i][j] += moonsVel[i][j]
  
  energy = 0
  for i in range(len(moonsPos)):
    pot = sum([abs(moonsPos[i][x]) for x in range(3)])
    kin = sum([abs(moonsVel[i][x]) for x in range(3)])
    energy += pot * kin
  
  print((time() - s) * 1000, 'ms')