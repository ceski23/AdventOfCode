import re


def run():
    with open('inputs/2.txt') as f:
        lines = f.readlines()
        validPasswords = 0

        for line in lines:
            match = re.match(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', line)
            pos1 = int(match.group(1))
            pos2 = int(match.group(2))
            letter = match.group(3)
            password = match.group(4)

            if (password[pos1-1] == letter) ^ (password[pos2-1] == letter):
                validPasswords += 1

        return validPasswords


if __name__ == "__main__":
    print(run())
