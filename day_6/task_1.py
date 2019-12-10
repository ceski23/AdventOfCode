def countOrbits(orbitsMap, a):
  return 0 if a not in orbitsMap else 1 + countOrbits(orbitsMap, orbitsMap[a])

with open('input.txt') as f:
  orbitsMap = {}
  for line in f:
    a, b = line.strip().split(')')
    orbitsMap[b] = a

  orbits = [countOrbits(orbitsMap, a) for a in orbitsMap]
  print(sum(orbits))