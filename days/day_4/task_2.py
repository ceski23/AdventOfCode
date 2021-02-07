from helpers import read_input
import re

expected_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

pattern = re.compile(r'(\w{3}):(.*?)(?:\s|$)')


def validator(field, value):
    if field == 'byr':
        return 1920 <= int(value) <= 2002
    elif field == 'iyr':
        return 2010 <= int(value) <= 2020
    elif field == 'eyr':
        return 2020 <= int(value) <= 2030
    elif field == 'hgt':
        return bool(re.match(r'^(1([5-8][0-9]|9[0-3])cm)|((59|6[0-9]|7[0-6])in)$', value))
    elif field == 'hcl':
        return bool(re.match(r'^#[a-f0-9]{6}$', value))
    elif field == 'ecl':
        return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    elif field == 'pid':
        return bool(re.match(r'^[0-9]{9}$', value))
    return False


def run(data):
    fields = set(expected_fields)
    valid_passports = 0

    for line in data:
        results = re.findall(pattern, line)
        if len(results) == 0:
            if len(fields) == 0:
                valid_passports += 1
            fields = set(expected_fields)
        else:
            for field, value in results:
                if field in fields and validator(field, value):
                    fields.remove(field)
    if len(fields) == 0:
        valid_passports += 1
    return valid_passports


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 186


def test_test():
    assert run(read_input('test.txt')) == 2


def test_invalid():
    assert run(read_input('invalid_passports.txt')) == 0


def test_valid():
    assert run(read_input('valid_passports.txt')) == 4
