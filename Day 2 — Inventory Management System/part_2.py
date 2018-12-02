lines = open('input.txt').read().splitlines()

for line in lines:
  for cmpLine in lines:
    diff = [c1 != c2 for c1, c2 in zip(line, cmpLine)]
    
    if sum(diff) == 1:
      letters = [c for c, b in zip(line, diff) if not b]
      print(''.join(letters))
      quit()