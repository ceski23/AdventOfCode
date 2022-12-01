import esMain from "es-main";
import * as R from "ramda";
import { parseInput } from "days/day1";

const calcTopNCalories = (inventories: number[][], n: number) => {
  const topSummedInventories = inventories
    .map(R.sum)
    .sort(R.descend(R.identity))
    .slice(0, n);

  return R.sum(topSummedInventories);
};

if (esMain(import.meta)) {
  const testInput = await parseInput("./test.txt");
  console.log("TEST:", calcTopNCalories(testInput, 3));

  const input = await parseInput("./input.txt");
  console.log("INPUT:", calcTopNCalories(input, 3));
}
