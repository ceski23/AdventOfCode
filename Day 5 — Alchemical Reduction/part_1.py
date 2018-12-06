polymer = list(open('input.txt').read())
i = 0

while (i < len(polymer)):
  if i+1 < len(polymer) and abs(ord(polymer[i]) - ord(polymer[i+1])) == 32:
    del polymer[i:i+2]
    i -= 1 if i-1 >= 0 else 0
  else: i += 1

print(len(polymer))