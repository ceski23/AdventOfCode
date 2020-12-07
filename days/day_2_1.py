import re


def run():
    with open('inputs/2.txt') as f:
        lines = f.readlines()
        validPasswords = 0

        for line in lines:
            match = re.match(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', line)
            minimum = int(match.group(1))
            maximum = int(match.group(2))
            letter = match.group(3)
            password = match.group(4)

            counter = 0
            for char in password:
                if char == letter:
                    counter += 1

            if counter >= minimum and counter <= maximum:
                validPasswords += 1

        return validPasswords


if __name__ == "__main__":
    print(run())
