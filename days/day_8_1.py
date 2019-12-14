import numpy as np

with open('inputs/8.txt') as f:
  width, height = (25, 6)
  layers = []
  while (data := f.read(width * height)):
    layers.append(np.reshape(list(map(int, list(data))), (width, height)))

  temp = [np.sum(layer == 0) for layer in layers]
  zeroLayer = temp.index(min(temp))
  
  checksum = np.sum(layers[zeroLayer] == 1) * np.sum(layers[zeroLayer] == 2)
  print(checksum)