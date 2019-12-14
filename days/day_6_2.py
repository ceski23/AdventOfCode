def findWay(orbitsMap, a):
  way, curr = [a], a
  while curr in orbitsMap:
    way.append(orbitsMap[curr])
    curr = orbitsMap[curr]
  return way

def findCommonRoot(way1, way2):
  way1, way2 = way1[::-1], way2[::-1]
  for i in range(min(len(way1), len(way2))):
    if (way1[i] != way2[i]):
      return way1[i-1]
  return None

def countOrbits(orbitsMap, a, b):
  return 0 if (a not in orbitsMap or a == b) else 1 + countOrbits(orbitsMap, orbitsMap[a], b)

with open('inputs/6.txt') as f:
  orbitsMap = {}
  for line in f:
    a, b = line.strip().split(')')
    orbitsMap[b] = a

  myOrbit = orbitsMap['YOU']
  santaOrbit = orbitsMap['SAN']

  way1, way2 = findWay(orbitsMap, myOrbit), findWay(orbitsMap, santaOrbit)
  rt = findCommonRoot(way1, way2)
  transfers = countOrbits(orbitsMap, myOrbit, rt) + countOrbits(orbitsMap, santaOrbit, rt)
  print(transfers)