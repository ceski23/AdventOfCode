import numpy as np

with open('inputs/8.txt') as f:
  size = (6, 25)
  layers = []
  while (data := f.read(size[0] * size[1])):
    layers.append(np.reshape(list(map(int, list(data))), size))

  image = np.full(size, 2)
  for layer in layers:
    transparentPixels = (image == 2)
    image[transparentPixels] = layer[transparentPixels]

  for line in image:
    for x in map(str, line.tolist()):
      print('#' if x == '1' else ' ', end='')
    print()