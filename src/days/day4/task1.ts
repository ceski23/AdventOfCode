import esMain from "es-main";
import { readFile } from "fs/promises";
import * as R from "ramda";

export type Pair<A, B = A> = [A, B];
export type Range = Pair<number>;

export const parseInput = async (
  path: string
): Promise<Pair<Range, Range>[]> => {
  const data = await readFile(new URL(path, import.meta.url), "utf-8");

  return data.split("\n").map((line) => {
    const match = line.match(/(\d+)-(\d+),(\d+)-(\d+)/);

    return [
      [Number(match![1]), Number(match![2])],
      [Number(match![3]), Number(match![4])],
    ];
  });
};

const isFullyContained = (pair: Pair<Range>) => {
  const [[s1, e1], [s2, e2]] = pair;

  return (s1 >= s2 && e1 <= e2) || (s2 >= s1 && e2 <= e1);
};

const calcContainedPairs = (pairs: Pair<Range>[]) => {
  return R.count(isFullyContained, pairs);
};

if (esMain(import.meta)) {
  console.log(calcContainedPairs(await parseInput("./test.txt")));
  console.log(calcContainedPairs(await parseInput("./input.txt")));
}
