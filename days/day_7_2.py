import re

rulePattern = re.compile(r'(\w+ \w+) bags contain (?:(\d+.*)|no other bags).')
bagPattern = re.compile(r'(\d+) (\w+ \w+) bags?')


def find(graph, node, qty=1):
    if len(graph[node]) == 0:
        return qty
    else:
        c = 0
        for quantity, bag in graph[node]:
            c += find(graph, bag, int(quantity))
        return (c * qty) + qty


def run():
    with open('inputs/7.txt') as f:
        wardrobe = {}
        for line in f:
            source, target = rulePattern.search(line).groups()
            if source not in wardrobe:
                wardrobe[source] = []
            if target:
                bags = bagPattern.findall(target)
                for bag in bags:
                    wardrobe[source].append(bag)

        return find(wardrobe, 'shiny gold') - 1


if __name__ == "__main__":
    print(run())
