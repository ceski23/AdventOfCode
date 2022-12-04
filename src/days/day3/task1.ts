import * as R from "ramda";
import esMain from "es-main";
import { readFile } from "fs/promises";
import { match } from "ts-pattern";

export const nonNullable = <T>(value: T): value is NonNullable<T> =>
  value !== undefined && value !== null;

export const parseInput = async (path: string) => {
  const data = await readFile(new URL(path, import.meta.url), "utf-8");

  return data.split("\n");
};

const findSharedItem = (rucksack: string) => {
  const [first, second] = R.splitAt(rucksack.length / 2, rucksack).map(
    (items) => Array.from(items)
  );

  return R.intersection(first, second).at(0);
};

export const calcPriority = (item: string) =>
  match(item.charCodeAt(0))
    .when(R.both(R.gte(R.__, 97), R.lte(R.__, 122)), (val) => val - 96)
    .when(R.both(R.gte(R.__, 65), R.lte(R.__, 90)), (val) => val - 38)
    .otherwise(() => {
      throw new Error("Invalid item");
    });

const calcPriorities = (rucksacks: string[]) => {
  const prorities = rucksacks
    .map(findSharedItem)
    .filter(nonNullable)
    .map(calcPriority);

  return R.sum(prorities);
};

if (esMain(import.meta)) {
  console.log(calcPriorities(await parseInput("./test.txt")));
  console.log(calcPriorities(await parseInput("./input.txt")));
}
