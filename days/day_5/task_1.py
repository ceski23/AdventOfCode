from pathlib import Path
import os
from dataclasses import dataclass
from typing import Tuple
import re
from collections import Counter


@dataclass
class Cloud:
    start: Tuple[int, int]
    end: Tuple[int, int]

    def is_horizontal_or_vertical(self):
        return self.start[0] == self.end[0] or self.start[1] == self.end[1]


def parse_input(path: str):
    with Path(os.path.dirname(__file__), path).open() as f:
        input_pattern = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
        clouds: list[Cloud] = []
        for line in f:
            if match := input_pattern.match(line):
                x1, y1, x2, y2 = match.groups()
                cloud = Cloud((int(x1), int(y1)), (int(x2), int(y2)))
                clouds.append(cloud)
    return clouds


def create_clouds_map(clouds: list[Cloud]):
    map: Counter[Tuple[int, int]] = Counter()
    for cloud in clouds:
        if cloud.is_horizontal_or_vertical():
            step_x = 1 if cloud.start[0] <= cloud.end[0] else -1
            step_y = 1 if cloud.start[1] <= cloud.end[1] else -1
            for x in range(cloud.start[0], cloud.end[0] + step_x, step_x):
                for y in range(cloud.start[1], cloud.end[1] + step_y, step_y):
                    map[(x, y)] += 1
    return map


def count_overlaped(clouds_map: Counter[Tuple[int, int]]):
    return sum(count > 1 for count in clouds_map.values())


if __name__ == "__main__":
    clouds = parse_input('input.txt')
    clouds_map = create_clouds_map(clouds)
    print(count_overlaped(clouds_map))
