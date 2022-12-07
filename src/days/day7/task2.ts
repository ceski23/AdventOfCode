import esMain from "es-main";
import { DirectoryTraversal, parseInput } from "./task1";

const findDirectoryToDelete = (stats: Record<string, number>) => {
  const totalDiskSpace = 70000000;
  const updateSize = 30000000;
  const usedSpace = stats["/"];
  const unusedSpace = totalDiskSpace - usedSpace;
  const spaceToFreeUp = updateSize - unusedSpace;

  const [, size] = Object.entries(stats)
    .sort(([, a], [, b]) => a - b)
    .find(([, size]) => size >= spaceToFreeUp)!;

  return size;
};

if (esMain(import.meta)) {
  const testInput = await parseInput("./test.txt");
  console.log(
    "TEST:",
    findDirectoryToDelete(new DirectoryTraversal().run(testInput))
  );

  const input = await parseInput("./input.txt");
  console.log(
    "INPUT:",
    findDirectoryToDelete(new DirectoryTraversal().run(input))
  );
}
