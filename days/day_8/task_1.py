from pathlib import Path
import os
from dataclasses import dataclass
import re
from typing import Dict, Set


@dataclass
class Digit:
    signals: set[str]


class Entry:
    signal_patterns: list[Digit]
    output_signals: list[Digit]
    mappings: Dict[str, Set[str]]

    def __init__(self, signal_patterns: list[Digit], output_signals: list[Digit]) -> None:
        self.signal_patterns = signal_patterns
        self.output_signals = output_signals


def parse_input(path: str):
    pattern = re.compile(r'([a-g]+)')
    entries: list[Entry] = []

    with Path(os.path.dirname(__file__), path).open() as f:
        for line in f:
            signals = pattern.findall(line)
            entries.append(Entry(
                [Digit(set(x)) for x in signals[:10]], [Digit(set(x))
                                                        for x in signals[10:]]
            ))
    return entries


def count_1_4_7_8(entries: list[Entry]):
    counter = 0
    for entry in entries:
        for digit in entry.output_signals:
            if len(digit.signals) in [2, 3, 4, 7]:
                counter += 1
    return counter


if __name__ == "__main__":
    entries = parse_input('input.txt')
    print(count_1_4_7_8(entries))
