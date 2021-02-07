from helpers import read_input
import re


def run(data):
    validPasswords = 0

    for line in data:
        match = re.match(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', line)
        pos1 = int(match.group(1))
        pos2 = int(match.group(2))
        letter = match.group(3)
        password = match.group(4)

        if (password[pos1-1] == letter) ^ (password[pos2-1] == letter):
            validPasswords += 1

    return validPasswords


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 482


def test_test():
    assert run(read_input('test.txt')) == 1
