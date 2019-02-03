from operator import itemgetter

lines = open('input.txt').read().splitlines()
points = [tuple(map(int, line.split(', '))) for line in lines]

minX, minY = min(points, key=itemgetter(0))[0], min(points, key=itemgetter(1))[1]
maxX, maxY = max(points, key=itemgetter(0))[0], max(points, key=itemgetter(1))[1]
w, h = maxX - minX + 1, maxY - minY + 1

size = 0
for x in range(w):
  for y in range(h):
    distSum = 0
    for p in points:
      distSum += abs(x - (p[0]-minX)) + abs(y - (p[1]-minY))
    if distSum < 10000: size += 1

print(size)