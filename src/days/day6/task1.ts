import esMain from "es-main";
import { readFile } from "fs/promises";
import * as R from "ramda";

export const parseInput = async (path: string) => {
  const data = await readFile(new URL(path, import.meta.url), "utf-8");

  return Array.from(data.trim());
};

const slidingWindow = <T>(array: T[], size: number) =>
  Array.from({ length: array.length - size + 1 }, (_, index) =>
    array.slice(index, index + size)
  );

const areAllValuesUniqe = <T>(array: T[]) =>
  R.uniq(array).length === array.length;

export const findMarkerPosition = (data: string[], seqLength: number) => {
  const idx = slidingWindow(data, seqLength).findIndex(areAllValuesUniqe);
  return idx + seqLength;
};

if (esMain(import.meta)) {
  console.log("TEST:", findMarkerPosition(await parseInput("./test.txt"), 4));
  console.log("INPUT:", findMarkerPosition(await parseInput("./input.txt"), 4));
}
