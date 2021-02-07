from helpers import read_input
import re
from itertools import chain

rule_pattern = re.compile(r'^(.+): (\d+)-(\d+) or (\d+)-(\d+)$')


def parse_data(data):
    rules = {}
    my_ticket = None
    nearby_tickets = []
    i = 0

    for i, line in enumerate(data):
        if len(line) == 0:
            break
        else:
            match = rule_pattern.search(line).groups()
            field = match[0]
            range_1, range_2 = range(int(match[1]), int(
                match[2])+1), range(int(match[3]), int(match[4])+1)
            full_range = list(chain(range_1, range_2))
            rules[field] = full_range

    my_ticket = [int(n) for n in data[i+2].split(',')]

    for i, line in enumerate(data[i+5:]):
        ticket = [int(n) for n in line.split(',')]
        nearby_tickets.append(ticket)

    return rules, my_ticket, nearby_tickets


def check_ticket_valid(ticket, rules):
    for number in ticket:
        valid = False
        for field, valid_range in rules.items():
            if number in valid_range:
                valid = True
        if not valid:
            return False, number
    return True, None


def run(data):
    rules, my_ticket, nearby_tickets = parse_data(data)
    invalid_fields = []

    for ticket in nearby_tickets:
        valid, number = check_ticket_valid(ticket, rules)
        if not valid:
            invalid_fields.append(number)
    return sum(invalid_fields)


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 814


def test_test():
    assert run(read_input('test.txt')) == 71
