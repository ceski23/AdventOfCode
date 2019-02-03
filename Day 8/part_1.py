data = list(map(int, open('input.txt').read().split(' ')))

def getData(c=ord('A'), nodes={}):
  meta, nodes_num, meta_num = [], data.pop(0), data.pop(0)
  for x in range(nodes_num):
    getData(c+x+1)

  for x in range(meta_num):
    meta.append(data.pop(0))

  nodes[chr(c)] = meta
  return 

getData()
print(nodes)

suma = sum([sum(x) for x in nodes.values()])
print(suma)