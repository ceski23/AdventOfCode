import esMain from "es-main";
import { readFile } from "fs/promises";
import * as R from "ramda";
import { nonNullable } from "utils";

export type Procedure = {
  count: number;
  from: number;
  to: number;
};

export const parseInput = async (path: string) => {
  const data = await readFile(new URL(path, import.meta.url), "utf-8");
  const [rawCrates, rawProcedures] = data.split("\n\n");

  const crates = R.transpose(
    rawCrates
      .split("\n")
      .slice(0, -1)
      .map((line) =>
        Array.from(line.matchAll(/(?:\[([A-Z])\]|\s(\s)\s)\s?/g)).map((match) =>
          match.at(1)
        )
      )
  ).map((stack) => R.reverse(stack.filter(nonNullable)));

  const procedures = rawProcedures.split("\n").map<Procedure>((line) => {
    const [_, count, from, to] = line
      .match(/move (\d+) from (\d+) to (\d+)/)!
      .map(Number);
    return { count, from, to };
  });

  return {
    crates,
    procedures,
  };
};

const executeProcedure = (
  cargo: string[][],
  { count, from, to }: Procedure,
  oneByOne: boolean = true
) =>
  R.compose(
    R.update(
      from - 1,
      cargo[from - 1].slice(0, cargo[from - 1].length - count)
    ),
    R.update(
      to - 1,
      cargo[to - 1].concat(
        oneByOne
          ? R.reverse(cargo[from - 1].slice(-count))
          : cargo[from - 1].slice(-count)
      )
    )
  )(cargo);

export const moveCrates = (
  crates: string[][],
  procedures: Procedure[],
  oneByOne: boolean = true
) =>
  procedures.reduce(
    (cargo, procedure) => executeProcedure(cargo, procedure, oneByOne),
    crates
  );

export const readTopOfCargo = (crates: string[][]) =>
  crates.map((stack) => stack.at(-1)).join("");

if (esMain(import.meta)) {
  const testInput = await parseInput("./test.txt");
  console.log(
    readTopOfCargo(moveCrates(testInput.crates, testInput.procedures))
  );

  const input = await parseInput("./input.txt");
  console.log(readTopOfCargo(moveCrates(input.crates, input.procedures)));
}
