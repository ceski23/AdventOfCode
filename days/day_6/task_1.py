from pathlib import Path
import os


def parse_input(path: str):
    with Path(os.path.dirname(__file__), path).open() as f:
        return [int(n) for n in f.readline().split(',')]


def simulate_lanternfishes(fishes: list[int]):
    while True:
        new_fishes = 0
        for i, fish in enumerate(fishes):
            match fish:
                case 0:
                    new_fishes += 1
                    fishes[i] = 6
                case n:
                    fishes[i] = n - 1
        fishes.extend([8] * new_fishes)
        yield fishes


def run_simulation(fishes: list[int], iterations: int):
    simulator = simulate_lanternfishes(fishes)
    return next(x for i, x in enumerate(simulator) if i == iterations - 1)


if __name__ == "__main__":
    fishes = parse_input('input.txt')
    simulator = simulate_lanternfishes(fishes)
    print(len(run_simulation(fishes, 80)))
