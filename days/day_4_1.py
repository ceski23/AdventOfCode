import re

expected_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

pattern = re.compile(r'(\w{3}):(.*?)(?:\s|$)')


def run():
    with open('inputs/4.txt') as f:
        fields = set(expected_fields)
        valid_passports = 0

        for line in f:
            results = re.findall(pattern, line)
            if len(results) == 0:
                if len(fields) == 0:
                    valid_passports += 1
                fields = set(expected_fields)
            else:
                for field, value in results:
                    if field in fields:
                        fields.remove(field)
        if len(fields) == 0:
            valid_passports += 1
        return valid_passports


if __name__ == "__main__":
    print(run())
