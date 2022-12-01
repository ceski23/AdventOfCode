import esMain from "es-main";
import { readFile } from "fs/promises";
import * as R from "ramda";

export const parseInput = async (path: string) => {
  const data = await readFile(new URL(path, import.meta.url), "utf-8");
  return data
    .split("\n\n")
    .map((inventory) => inventory.split("\n").map(Number));
};

const calcMostCalories = (inventories: number[][]) => {
  return R.sum(inventories.reduce(R.maxBy(R.sum)));
};

if (esMain(import.meta)) {
  const testInput = await parseInput("./test.txt");
  console.log("TEST:", calcMostCalories(testInput));

  const input = await parseInput("./input.txt");
  console.log("INPUT:", calcMostCalories(input));
}
