from task_1 import parse_input, count_overlaped, Cloud, Counter
from typing import Tuple


def create_clouds_map(clouds: list[Cloud]):
    map: Counter[Tuple[int, int]] = Counter()
    for cloud in clouds:
        step_x = 1 if cloud.start[0] <= cloud.end[0] else -1
        step_y = 1 if cloud.start[1] <= cloud.end[1] else -1
        xs = range(cloud.start[0], cloud.end[0] + step_x, step_x)
        ys = range(cloud.start[1], cloud.end[1] + step_y, step_y)
        if cloud.is_horizontal_or_vertical():
            for x in xs:
                for y in ys:
                    map[(x, y)] += 1
        else:
            for x, y in zip(xs, ys):
                map[(x, y)] += 1
    return map


if __name__ == "__main__":
    clouds = parse_input('input.txt')
    clouds_map = create_clouds_map(clouds)
    print(count_overlaped(clouds_map))
