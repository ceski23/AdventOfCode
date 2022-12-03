import esMain from "es-main";
import { readFile } from "fs/promises";
import * as R from "ramda";
import { match } from "ts-pattern";

export type Move = "rock" | "paper" | "scissors";

export const parseMove = (move: string) =>
  match<string, Move>(move)
    .with("A", "X", () => "rock")
    .with("B", "Y", () => "paper")
    .with("C", "Z", () => "scissors")
    .otherwise(() => {
      throw new Error("Unknown move");
    });

const calcMoveScore = (move: Move) =>
  match<Move, number>(move)
    .with("rock", () => 1)
    .with("paper", () => 2)
    .with("scissors", () => 3)
    .exhaustive();

const parseInput = async (path: string) => {
  const data = await readFile(new URL(path, import.meta.url), "utf-8");
  const rounds = data
    .split("\n")
    .map((moves) => moves.split(" ").map(parseMove));

  return rounds;
};

export const calcRoundScore = (moves: Move[]) => {
  const [opponentMove, yourMove] = moves;
  const moveScore = calcMoveScore(yourMove);

  const resultScore = match([yourMove, opponentMove])
    .when(
      () => yourMove === opponentMove,
      () => 3
    )
    .with(
      ["rock", "scissors"],
      ["paper", "rock"],
      ["scissors", "paper"],
      () => 6
    )
    .otherwise(() => 0);

  return moveScore + resultScore;
};

export const simulateTournament = (rounds: Move[][]) => {
  const roundsScores = rounds.map(calcRoundScore);
  return R.sum(roundsScores);
};

if (esMain(import.meta)) {
  const testInput = await parseInput("./test.txt");
  console.log(simulateTournament(testInput));

  const input = await parseInput("./input.txt");
  console.log(simulateTournament(input));
}
