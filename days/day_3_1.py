import numpy as np
import matplotlib.pyplot as plt

def decodeDir(x):
  val = int(x[1:])
  return {
    'R': (val, 0),
    'U': (0, val),
    'L': (-val, 0),
    'D': (0, -val)
  }[x[0]]

def getPoints(directions):
  vec = [(0, 0)]
  for x in directions:
    last = vec[-1]
    new = decodeDir(x)
    vec.append((last[0] + new[0], last[1] + new[1]))
  return vec

def findIntersection(p1, p2, p3, p4):
  x1, y1 = p1
  x2, y2 = p2
  x3, y3 = p3
  x4, y4 = p4
  try:
    px = ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) ) 
    py = ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
    if (
      (px < max( min(x1,x2), min(x3,x4) )) or
      (px > min( max(x1,x2), max(x3,x4) )) or
      (py < max( min(y1,y2), min(y3,y4) )) or
      (py > min( max(y1,y2), max(y3,y4) ))
    ):
      return False
    else:
      return (int(px), int(py))
  except ZeroDivisionError:
    return False

def findIntersectionPoints(vec1, vec2):
  points = []
  for p1, p2 in zip(vec1[:], vec1[1:]):
    for p3, p4 in zip(vec2[:], vec2[1:]):
      inter = findIntersection(p1, p2, p3, p4)
      if inter:
        points.append(inter)
        plt.plot(*inter, marker='o')
  return points[1:]

with open('inputs/3.txt') as f:
  vec1 = getPoints(f.readline().split(','))
  vec2 = getPoints(f.readline().split(','))

  for p1, p2 in zip(vec1[:], vec1[1:]):
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='r')
  for p3, p4 in zip(vec2[:], vec2[1:]):
    plt.plot([p3[0], p4[0]], [p3[1], p4[1]], color='g')

  intersections = findIntersectionPoints(vec1, vec2)
  out = min([abs(p[0]) + abs(p[1]) for p in intersections])
  print(out)
  plt.show()