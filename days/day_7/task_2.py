from helpers import read_input
from days.day_7.task_1 import rulePattern, bagPattern


def find(graph, node):
    if len(graph[node]) == 0:
        return 1
    else:
        c = 1
        for quantity, bag in graph[node]:
            c += int(quantity) * find(graph, bag)
        return c


def run(data):
    wardrobe = {}
    for line in data:
        source, target = rulePattern.search(line).groups()
        if source not in wardrobe:
            wardrobe[source] = []
        if target:
            bags = bagPattern.findall(target)
            for bag in bags:
                wardrobe[source].append(bag)

    return find(wardrobe, 'shiny gold') - 1


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 7867


def test_1():
    assert run(read_input('test_1.txt')) == 32


def test_2():
    assert run(read_input('test_2.txt')) == 126
