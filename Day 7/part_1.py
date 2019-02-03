from operator import itemgetter
import re
from collections import OrderedDict

def dfs(graph, start, visited=None):
  if visited is None: visited = OrderedDict()
  visited[start] = None
  for nxt in sorted(graph[start] - set(visited.keys())):
    dfs(graph, nxt, visited)
  return visited

pattern = r'\b([A-Z])\b.*\b([A-Z])\b'
graph, steps = {}, set()
result = []

f = open('input.txt')
for line in f:
  s1, s2 = re.search(pattern, line).groups()
  if s1 not in graph: graph[s1] = set()
  if s2 not in graph: graph[s2] = set()
  graph[s1].add(s2)
  steps.add(s1)
  steps.add(s2)

# print(graph)

# inverted_graph = {}
# for key, values in graph.items():
#   if key not in inverted_graph: inverted_graph[key] = set()
#   for value in values:
#     if value not in inverted_graph: inverted_graph[value] = set()
#     inverted_graph[value].add(key)

while (len(steps) > 0):
  vals = set()
  # end = None
  for key, values in graph.items():
    vals.update(values)
    # if len(values) == 0: end = key

  toRemove = steps - vals
  print(toRemove)
  for i in toRemove:
    del graph[i]
    steps.remove(i)
  # print(end)



# print(inverted_graph)

# start = next(iter(inverted_graph.keys()))
# while (start in inverted_graph.keys()):
#   start = next(iter(inverted_graph[start]))

# end = next(iter(graph.keys()))
# while (end in graph.keys()):
#   end = next(iter(graph[end]))

# print(start, end)

# print(dfs(graph, 'C'))

# start = list(graph.keys())[0]
# result = dfs(graph, start)
# del result[end]
# result[end] = None
# print(''.join(result.keys()))
