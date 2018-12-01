output = 0
seen = {0: True}

f = open('input.txt', 'r')
while (True):
  for line in f.readlines():
    output += int(line)

    if output in seen:
      print(output)
      quit()
    else:
      seen[output] = True
      
  f.seek(0)