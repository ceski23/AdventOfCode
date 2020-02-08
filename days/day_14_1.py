import re
import math

def craft(recipes, backpack, quantity, what, amount=1, nest=1):
  print(nest*'\t' + f'I need {amount} of {what}, crafting...')
  x = 0
  for n, ingredient in recipes[what]:
    if ingredient not in recipes:
      z = math.ceil(int(amount) / quantity[what])
      x += z * int(n)
    else:
      x += craft(recipes, backpack, quantity, ingredient, n, nest+1)
  print(nest*'\t' + f'To make {amount} of {what} I need {x} ORE', x*int(amount))
  return x

with open('inputs/14.txt') as f:
  recipes, quantity = {}, {}
  backpack = {}
  for line in f:
    match = list(map(lambda x: x.split(' '), re.findall(r'(\d+ \w+)', line)))
    recipes[match[-1][1]] = match[:-1]
    quantity[match[-1][1]] = int(match[-1][0])
  print(craft(recipes, backpack, quantity, 'FUEL'))