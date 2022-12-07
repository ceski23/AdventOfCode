import esMain from "es-main";
import { readFile } from "fs/promises";
import * as R from "ramda";

export const parseInput = async (path: string) => {
  const data = await readFile(new URL(path, import.meta.url), "utf-8");
  return data.split("\n");
};

const directoryPath = (cwd: string[]) => {
  return cwd.join("/").replace("//", "/");
};

export class DirectoryTraversal {
  input: string[] = [];
  cwd: string[] = [];
  sizes: Record<string, number> = {};
  changeDirectoryCommandPattern = /\$ cd (.*?)$/;
  listCommandPattern = /\$ ls$/;

  run(commands: string[]) {
    this.input = commands;

    while (this.input.length > 0) {
      const command = this.input.shift();
      if (command) this.runCommand(command);
    }

    return this.sizes;
  }

  runCommand(command: string) {
    if (this.changeDirectoryCommandPattern.test(command)) {
      const [, directory] = command.match(this.changeDirectoryCommandPattern)!;
      this.changeDirectory(directory);
    } else if (this.listCommandPattern.test(command)) {
      this.list();
    } else {
      console.log(`Unknown command "${command}". Ignoring`);
    }
  }

  changeDirectory(directory: string) {
    if (directory === "..") {
      this.cwd.pop();
      return;
    }

    this.cwd.push(directory);
  }

  list() {
    while (
      !(this.input.at(0) === undefined || this.input.at(0)?.startsWith("$"))
    ) {
      const line = this.input.shift();
      const fileMatch = line?.match(/(\d+) (.*?)$/);

      if (fileMatch) {
        this.cwd.forEach((_, index, arr) => {
          const path = directoryPath(arr.slice(0, index + 1));
          this.sizes[path] = (this.sizes[path] ?? 0) + Number(fileMatch[1]);
        });
      }
    }
  }
}

const sumSizeOfDirectories = (
  stats: Record<string, number>,
  maxDirSize: number
) => {
  return R.sum(Object.values(stats).filter((size) => size <= maxDirSize));
};

if (esMain(import.meta)) {
  const testInput = await parseInput("./test.txt");
  console.log(
    "TEST:",
    sumSizeOfDirectories(new DirectoryTraversal().run(testInput), 100000)
  );

  const input = await parseInput("./input.txt");
  console.log(
    "INPUT:",
    sumSizeOfDirectories(new DirectoryTraversal().run(input), 100000)
  );
}
