import esMain from "es-main";
import { moveCrates, parseInput, Procedure, readTopOfCargo } from "./task1";

if (esMain(import.meta)) {
  const testInput = await parseInput("./test.txt");
  console.log(
    readTopOfCargo(moveCrates(testInput.crates, testInput.procedures, false))
  );

  const input = await parseInput("./input.txt");
  console.log(
    readTopOfCargo(moveCrates(input.crates, input.procedures, false))
  );
}
