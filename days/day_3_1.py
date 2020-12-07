def run():
    with open('inputs/3.txt') as f:
        geoMap = f.read().splitlines()
        x, y = 0, 0
        trees = 0

        while y < len(geoMap):
            if geoMap[y][x] == '#':
                trees += 1
            x = (x + 3) % len(geoMap[0])
            y += 1

        return trees


if __name__ == "__main__":
    print(run())
