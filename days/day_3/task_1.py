from pathlib import Path
import os


def parse_input(path: str):
    with Path(os.path.dirname(__file__), path).open() as f:
        numbers: list[str] = []
        for line in f:
            numbers.append(line.strip())
    return numbers


def calc_bits_frequency(numbers: list[str]):
    freq = [0 for _ in range(len(numbers[0]))]
    for n in numbers:
        for i, bit in enumerate(n):
            freq[i] += int(bit)
    return freq


if __name__ == "__main__":
    numbers = parse_input('input.txt')
    frequencies = calc_bits_frequency(numbers)
    gamma = ['1' if n >= (len(numbers) / 2) else '0' for n in frequencies]
    epsilon = ['1' if n < (len(numbers) / 2) else '0' for n in frequencies]
    print(int(''.join(gamma), 2) * int(''.join(epsilon), 2))
