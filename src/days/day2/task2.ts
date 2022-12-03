import { Move, parseMove, simulateTournament } from "days/day2";
import esMain from "es-main";
import { readFile } from "fs/promises";
import { match, P } from "ts-pattern";

enum Result {
  Loss = "X",
  Draw = "Y",
  Win = "Z",
}

const findProperMove = (opponentMove: Move, result: string) =>
  match<[string, Move], Move>([result, opponentMove])
    .with([Result.Draw, P._], () => opponentMove)
    .with([Result.Loss, "paper"], () => "rock")
    .with([Result.Loss, "rock"], () => "scissors")
    .with([Result.Loss, "scissors"], () => "paper")
    .with([Result.Win, "paper"], () => "scissors")
    .with([Result.Win, "rock"], () => "paper")
    .with([Result.Win, "scissors"], () => "rock")
    .otherwise(() => {
      throw new Error("Unknown result");
    });

const parseInput = async (path: string) => {
  const data = await readFile(new URL(path, import.meta.url), "utf-8");
  const rounds = data.split("\n").map((line) => {
    const [move, result] = line.split(" ");
    const opponentMove = parseMove(move);
    return [opponentMove, findProperMove(opponentMove, result)];
  });

  return rounds;
};

if (esMain(import.meta)) {
  const testInput = await parseInput("./test.txt");
  console.log(simulateTournament(testInput));

  const input = await parseInput("./input.txt");
  console.log(simulateTournament(input));
}
