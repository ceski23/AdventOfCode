from task_1 import parse_input
from itertools import islice


def simulate_lanternfishes(initial_fishes: list[int]):
    fishes = dict.fromkeys(range(9), 0)
    for fish in initial_fishes:
        fishes[fish] += 1

    while True:
        new_fishes = 0
        for timer, amount in fishes.items():
            match timer:
                case 0:
                    new_fishes = amount
                case n:
                    fishes[n-1] = fishes[n]
        fishes[8] = new_fishes
        fishes[6] += new_fishes
        yield fishes


def run_simulation(initial_fishes: list[int], iterations: int):
    simulator = simulate_lanternfishes(initial_fishes)
    return next(islice(simulator, iterations - 1, None))


if __name__ == "__main__":
    initial_fishes = parse_input('input.txt')
    print(sum(run_simulation(initial_fishes, 256).values()))
