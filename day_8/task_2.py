import numpy as np

def saveToImage(data, name):
  height, width = data.shape
  with open(name, 'w') as f:
    f.write('P1\n')
    f.write(f'{width} {height}\n')
    for line in data:
      f.write(' '.join(map(str, line.tolist())))
      f.write('\n')

with open('input.txt') as f:
  size = (6, 25)
  layers = []
  while (data := f.read(size[0] * size[1])):
    layers.append(np.reshape(list(map(int, list(data))), size))

  image = np.full(size, 2)
  for layer in layers:
    transparentPixels = (image == 2)
    image[transparentPixels] = layer[transparentPixels]

  saveToImage(image, 'image.pbm')