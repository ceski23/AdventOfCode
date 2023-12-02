import esMain from "es-main";
import { readFile } from "fs/promises";
import * as R from "ramda";

const parseInput = async (path: string) => {
  const data = await readFile(new URL(path, import.meta.url), "utf-8");

  return data.split("\n").map((row) => Array.from(row).map(Number));
};

const getColumn = (
  matrix: number[][],
  x: number,
  start: number,
  end: number
) => {
  const range = Array.from({ length: end - start }, (_, i) => i + start);
  return range.reduce((acc, y) => [...acc, matrix[y][x]], [] as number[]);
};

const getRow = (matrix: number[][], y: number, start: number, end: number) => {
  const range = Array.from({ length: end - start }, (_, i) => i + start);
  return range.reduce((acc, x) => [...acc, matrix[y][x]], [] as number[]);
};

const isTreeVisible = (forest: number[][], x: number, y: number) => {
  const height = forest.length;
  const width = forest[0].length;
  const tree = forest[y][x];

  const top = getColumn(forest, x, 0, y);
  const bottom = getColumn(forest, x, y + 1, height);
  const left = getRow(forest, y, 0, x);
  const right = getRow(forest, y, x + 1, width);

  return (
    Math.max(...top) < tree ||
    Math.max(...bottom) < tree ||
    Math.max(...left) < tree ||
    Math.max(...right) < tree
  );
};

const calcSideScore = (trees: number[], tree: number) => {
  const baseScore = trees.findIndex((val) => val >= tree);

  return baseScore === -1 ? trees.length : baseScore + 1;
};

const calcScore = (forest: number[][], x: number, y: number) => {
  const height = forest.length;
  const width = forest[0].length;
  const tree = forest[y][x];

  const top = getColumn(forest, x, 0, y);
  const bottom = getColumn(forest, x, y + 1, height);
  const left = getRow(forest, y, 0, x);
  const right = getRow(forest, y, x + 1, width);

  const topScore = calcSideScore(top.reverse(), tree);
  const bottomScore = calcSideScore(bottom, tree);
  const leftScore = calcSideScore(left.reverse(), tree);
  const rightScore = calcSideScore(right, tree);

  return topScore * bottomScore * leftScore * rightScore;
};

const countVisibleTrees = (forest: number[][]) => {
  const truthMap = forest.map((row, y) => {
    return row.map((_, x) => {
      return isTreeVisible(forest, x, y);
    });
  });

  const count = truthMap.reduce((acc, row) => {
    return acc + R.count(R.identity, row);
  }, 0);

  return count;
};

const maxScenicScore = (forest: number[][]) => {
  const score = forest.reduce(
    (acc, row, y) =>
      Math.max(acc, ...row.map((_, x) => calcScore(forest, x, y))),
    0
  );

  return score;
};

if (esMain(import.meta)) {
  console.log("TEST:", countVisibleTrees(await parseInput("./test.txt")));
  console.log("INPUT:", countVisibleTrees(await parseInput("./input.txt")));

  console.log("TEST:", maxScenicScore(await parseInput("./test.txt")));
  console.log("INPUT:", maxScenicScore(await parseInput("./input.txt")));
}
