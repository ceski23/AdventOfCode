from itertools import cycle, repeat, islice

with open('inputs/16.txt') as f:
  inp = list(map(int, f.read()))
  template = [0, 1, 0, -1]

  for _ in range(100):
    results = []
    for i in range(len(inp)):    
      pattern = cycle([y for x in template for y in repeat(x, i+1)])
      next(pattern)
      x = sum([n * p for n, p in zip(inp, islice(pattern, len(inp)))])
      results.append(int(str(x)[-1]))
    inp = results
  
  print(''.join(map(str, inp[:8])))