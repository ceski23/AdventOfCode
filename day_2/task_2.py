def runSimulation(memory, noun, verb):
  memory[1] = noun
  memory[2] = verb
  opPos = 0

  while (opPos < len(memory)):
    opcode, src1, src2, dest = memory[opPos : opPos + 4]
    if (opcode == 1):
      memory[dest] = memory[src1] + memory[src2]
    elif (opcode == 2):
      memory[dest] = memory[src1] * memory[src2]
    else:
      break

    opPos += 4
  return memory[0]

with open('input.txt') as f:
  memory = list(map(int, f.readline().split(',')))

  for noun in range(100):
    for verb in range(100):
      result = runSimulation(memory.copy(), noun, verb)
      if (result == 19690720):
        print(100 * noun + verb)
        exit()