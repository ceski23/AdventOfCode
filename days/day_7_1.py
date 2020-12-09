import re

rulePattern = re.compile(r'(\w+ \w+) bags contain (?:(\d+.*)|no other bags).')
bagPattern = re.compile(r'(\d+) (\w+ \w+) bags?')


def run():
    with open('inputs/7.txt') as f:
        wardrobe = {}
        for line in f:
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
    print(run())
