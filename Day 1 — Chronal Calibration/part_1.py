output = 0

f = open('input.txt', 'r')
for line in f.readlines():
  output += int(line)

print(output)