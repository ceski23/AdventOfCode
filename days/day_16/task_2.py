from helpers import read_input
from days.day_16.task_1 import parse_data, check_ticket_valid
import random


def findBRUTEFORCE(my_ticket, valid_tickets, rules):
    all_fields = set(rules.keys())
    ordered_fields = []

    for i in range(len(my_ticket)):
        matching_fields = all_fields.copy()
        for ticket in valid_tickets:
            for field in matching_fields.copy():
                # print(ticket[i], rules[matching_fields[0]])
                if ticket[i] not in rules[field]:
                    matching_fields.remove(field)
        if len(matching_fields) > 0:
            found_field = list(matching_fields)
            # all_fields.remove(found_field)
            ordered_fields.append(found_field)
        else:
            print(f'No matching field!', i)
            # return None
    return ordered_fields


def run(data):
    rules, my_ticket, nearby_tickets = parse_data(data)
    valid_tickets = [my_ticket]

    valid_tickets.extend(list(filter(
        lambda x: check_ticket_valid(x, rules)[0], nearby_tickets
    )))

    # for ticket in nearby_tickets:
    #     valid, _ = check_ticket_valid(ticket, rules)
    #     if valid:
    #         valid_tickets.append(ticket)

    # ordered_fields = None
    # while ordered_fields == None:
    #     random.shuffle(valid_tickets)
    ordered_fields = findBRUTEFORCE(
        my_ticket, valid_tickets.copy(), rules.copy()
    )

    return ordered_fields

    # for i in range(len(my_ticket)):
    #     matching_fields = all_fields.copy()
    #     for ticket in valid_tickets:
    #         for field in matching_fields.copy():
    #             # print(ticket[i], rules[matching_fields[0]])
    #             if ticket[i] not in rules[field]:
    #                 matching_fields.remove(field)
    #     if len(matching_fields) > 0:
    #         found_field = list(matching_fields)[0]
    #         all_fields.remove(found_field)
    #         ordered_fields.append(found_field)
    #     else:
    #         print(f'No matching field!', i)

    return ordered_fields


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    # assert run(read_input('input.txt')) == 814
    assert False


def test_test():
    assert run(read_input('test.txt')) == 71
