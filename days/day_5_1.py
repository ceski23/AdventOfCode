def parseArg(memory, mode, value):
  return value if (int(mode) == 1) else memory[value]

def paramsCount(opcode):
  return {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    99: 0
  }[opcode]

def getFunction(opcode):
  return {
    1: add,
    2: multiply,
    3: read,
    4: write
  }.get(opcode, halt)

def add(args):
  a, b, _ = args
  return (3, a+b)

def multiply(params):
  a, b, _ = params
  return (3, a*b)

def read(params):
  val = int(input('Type input: '))
  return (1, val)

def write(params):
  a, = params
  print('OUTPUT:', a)
  return None

def halt(*args):
  return False


with open('inputs/5.txt') as f:
  memory = list(map(int, f.readline().split(',')))
  opPos = 0

  while (opPos < len(memory)):
    command = str(memory[opPos])
    opcode = int(command[-2:])
    paramCount = paramsCount(opcode)
    params = command[:-2].zfill(paramCount)[::-1]
    args = [ parseArg(memory, params[i], memory[opPos + i + 1]) for i in range(paramCount) ]
    result = getFunction(opcode)(args)

    if result:
      offset, value = result
      if offset:
        memory[memory[opPos + offset]] = value
      else:
        memory[opPos + 1] = value
    
    if result == False:
      break

    opPos += paramCount + 1