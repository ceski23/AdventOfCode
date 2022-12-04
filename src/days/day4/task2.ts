import esMain from "es-main";
import * as R from "ramda";
import { parseInput, Pair, Range } from "./task1";

const isOverlapping = (pair: Pair<Range>) => {
  const [[s1, e1], [s2, e2]] = pair;

  return (e1 >= s2 && s1 <= e2) || (e2 >= s1 && s2 <= e1);
};

const calcOverlappingPairs = (pairs: Pair<Range>[]) => {
  return R.count(isOverlapping, pairs);
};

if (esMain(import.meta)) {
  console.log(calcOverlappingPairs(await parseInput("./test.txt")));
  console.log(calcOverlappingPairs(await parseInput("./input.txt")));
}
