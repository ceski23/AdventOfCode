twos, threes = 0, 0

for line in open('input.txt'):
  count = {}

  for letter in line:
    count[letter] = count[letter] + 1 if letter in count else 1
  
  if 2 in count.values(): twos += 1
  if 3 in count.values(): threes += 1

print(twos * threes)