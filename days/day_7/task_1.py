from helpers import read_input
import re

rulePattern = re.compile(r'(\w+ \w+) bags contain (?:(\d+.*)|no other bags).')
bagPattern = re.compile(r'(\d+) (\w+ \w+) bags?')


def run(data):
    wardrobe = {}
    for line in data:
        source, target = rulePattern.search(line).groups()
        if target:
            bags = bagPattern.findall(target)
            for bag in bags:
                if bag[1] not in wardrobe:
                    wardrobe[bag[1]] = []
                wardrobe[bag[1]].append(source)

    found = set()
    queue = ['shiny gold']
    while len(queue) > 0:
        node = queue.pop(0)
        if node != 'shiny gold':
            found.add(node)
        if node in wardrobe:
            queue.extend(wardrobe[node])
    return len(found)


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 268


def test_1():
    assert run(read_input('test_1.txt')) == 4
