import numpy as np

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
    vec.append((last[0] + x[0], last[1] + x[1]))
  return vec

def segmentIntersection(p1, p2, p3, p4):
  z = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
  if (z == 0):
    return False

  x = ( (p1[0]*p2[1]-p1[1]*p2[0])*(p3[0]-p4[0])-(p1[0]-p2[0])*(p3[0]*p4[1]-p3[1]*p4[0]) ) / z
  y = ( (p1[0]*p2[1]-p1[1]*p2[0])*(p3[1]-p4[1])-(p1[1]-p2[1])*(p3[0]*p4[1]-p3[1]*p4[0]) ) / z

  if (
    (x < max(min(p1[0], p2[0]), min(p3[0], p4[0]))) or
    (x > min(max(p1[0], p2[0]), max(p3[0], p4[0]))) or
    (y < max(min(p1[1], p2[1]), min(p3[1], p4[1]))) or
    (y > min(max(p1[1], p2[1]), max(p3[1], p4[1])))
  ): return False

  return np.array((int(x), int(y)))

def findIntersectionPoints(vec1, vec2):
  points = []
  for p1, p2 in zip(vec1[:], vec1[1:]):
    for p3, p4 in zip(vec2[:], vec2[1:]):
      if i := segmentIntersection(p1, p2, p3, p4) is not False:
        points.append(i)
  return points[1:]

def findMinMax(*points):
  minX, minY = 0, 0
  maxX, maxY = 0, 0

  for p in points:
    if (p[0] < minX): minX = p[0]
    if (p[1] < minY): minY = p[1]
    if (p[0] > maxX): maxX = p[0]
    if (p[1] > maxY): maxY = p[1]
    
  return (np.array((minX, minY)), np.array((maxX, maxY)))

with open('input.txt') as f:
  dir1 = [decodeDir(x) for x in f.readline().split(',')]
  dir2 = [decodeDir(x) for x in f.readline().split(',')]
  points1 = getPoints(dir1)
  points2 = getPoints(dir2)

  minPos, maxPos = findMinMax(*points1, *points2)
  startPos = np.abs(minPos)
  wires = np.zeros(np.abs(minPos) + np.abs(maxPos) + 1)

  for directions in [dir1, dir2]:
    pos, distance = np.copy(startPos), 0
    for d in directions:
      axis = 0 if abs(d[0]) > 0 else 1
      step = 1 if d[axis] > 0 else -1
      for i in range(0, d[axis], step):
        distance += 1
        pos[axis] += step
        wires[pos[0], pos[1]] += distance

  intersections = findIntersectionPoints(points1, points2)
  distances = [wires[x + startPos[0], y + startPos[1]] for x, y in intersections]
  print(int(min(distances)))
