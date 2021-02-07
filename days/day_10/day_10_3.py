import time
from itertools import permutations


def run():
    with open('inputs/10.txt') as f:
        adapters = sorted([int(x) for x in f])
        built_in = max(adapters) + 3
        adapters.append(0)
        adapters.append(built_in)

        x = []
        for i in range(3, len(adapters) + 1):
            print(i)
            x.extend(permutations(adapters, i))

        print(x)


if __name__ == "__main__":
    start_time = time.time()
    print(run())
    print("--- %s seconds ---" % (time.time() - start_time))
