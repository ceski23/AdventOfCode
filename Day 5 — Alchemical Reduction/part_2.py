polymer = open('input.txt').read()
shortest = len(polymer)

for c in 'abcdefghijklmnopqrstuvwxyz':
  i, poly = 0, list(polymer.replace(c, '').replace(c.upper(), ''))

  while (i < len(poly)):
    if i+1 < len(poly) and abs(ord(poly[i]) - ord(poly[i+1])) == 32:
      del poly[i:i+2]
      i -= 1 if i-1 >= 0 else 0
    else: i += 1

  if len(poly) < shortest: shortest = len(poly)

print(shortest)