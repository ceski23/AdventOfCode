import esMain from "es-main";
import * as R from "ramda";
import { calcPriority, nonNullable, parseInput } from "./task1";

const findCommonItems = (group: string[]) => {
  const sets = group
    .map((items) => Array.from(items))
    .reduce((acc, item) => R.intersection(acc, item));

  return sets.at(0);
};

const calcPriorities = (input: string[]) => {
  const groups = R.splitEvery(3, input);
  const commonItems = groups.map(findCommonItems).filter(nonNullable);

  return R.sum(commonItems.map(calcPriority));
};

if (esMain(import.meta)) {
  console.log(calcPriorities(await parseInput("./test.txt")));
  console.log(calcPriorities(await parseInput("./input.txt")));
}
