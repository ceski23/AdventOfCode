with open('inputs/2.txt') as f:
  memory = list(map(int, f.readline().split(',')))
  opPos = 0

  memory[1] = 12
  memory[2] = 2

  while (opPos < len(memory)):
    opcode, src1, src2, dest = memory[opPos : opPos + 4]
    if (opcode == 1):
      memory[dest] = memory[src1] + memory[src2]
    elif (opcode == 2):
      memory[dest] = memory[src1] * memory[src2]
    else:
      break

    opPos += 4
  
  print(memory[0])