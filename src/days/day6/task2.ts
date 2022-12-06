import esMain from "es-main";
import { findMarkerPosition, parseInput } from "./task1";

if (esMain(import.meta)) {
  console.log("TEST:", findMarkerPosition(await parseInput("./test.txt"), 14));
  console.log(
    "INPUT:",
    findMarkerPosition(await parseInput("./input.txt"), 14)
  );
}
