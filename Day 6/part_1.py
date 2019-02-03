from operator import itemgetter

lines = open('input.txt').read().splitlines()
points = [tuple(map(int, line.split(', '))) for line in lines]

minX, minY = min(points, key=itemgetter(0))[0], min(points, key=itemgetter(1))[1]
maxX, maxY = max(points, key=itemgetter(0))[0], max(points, key=itemgetter(1))[1]
w, h = maxX - minX + 1, maxY - minY + 1
grid, badPoints, area = [[() for y in range(h)] for x in range(w)], set(['.']), {}

for x in range(w):
  for y in range(h):
    for i, p in enumerate(points):
      dist = abs(x - (p[0]-minX)) + abs(y - (p[1]-minY))
      if dist == 0:
        grid[x][y] = (0, i)
        break
      elif grid[x][y] == () or dist < grid[x][y][0]: grid[x][y] = (dist, i)
      elif grid[x][y][0] == dist: grid[x][y] = (dist, '.')
    if x in (0, w-1) or y in (0, h-1): badPoints.add(grid[x][y][1])

for x in range(w):
  for y in range(h):
    c = grid[x][y][1]
    if c not in badPoints:
      if c not in area: area[c] = 0
      area[c] += 1

print(max(area.values()))