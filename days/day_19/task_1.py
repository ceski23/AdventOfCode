from helpers import read_input
import re


pat = re.compile(r'^(\d+): ("\w"|[\d \|]+)')


def parse_data(data):
    rules_finished = False
    sequences = []
    rules = {}

    for line in data:
        if rules_finished:
            sequences.append(line)
        else:
            if len(line) == 0:
                rules_finished = True
            else:
                idx, value = pat.search(line).groups()
                if '"' in value:
                    rules[idx] = [value.split('"')[1]]
                elif '|' in value:
                    values = set([x.strip().split(' ')
                                  for x in value.split('|')])
                    rules[idx] = values
                else:
                    values = value.split(' ')
                    rules[idx] = values
    return rules, sequences


def x(seq, rules_seq, all_rules):

    for rule in rules_seq:
        if rule == 'a' or rule == 'b':
            if seq[0] == rule:
                seq = seq[1:]
            else:
                return False
        elif isinstance(rule, list):
            seq = x(seq, rule, all_rules)
            if seq == False:
                return False
        else:
            seq = x(seq, all_rules[rule], all_rules)
            if seq == False:
                return False

    return seq


def check(sequence, rules, rules_x):
    for rule in rules_x:
        print('rules[rule]:', rules[rule])
        if isinstance(rules[rule], list):
            seq = [check(sequence, rules, sub_rule)
                   for sub_rule in rules[rule]]
            if any(seq):
                sequence = filter(lambda x: x, seq)
        elif rules[rule] != 'a' and rules[rule] != 'b':
            sequence = check(sequence, rules, rule)
            if sequence == False:
                return False
        else:
            if sequence[0] != rules[rule]:
                return False
            else:
                sequence = sequence[1:]


def run(data):
    rules, sequences = parse_data(data)
    # return check(sequences[0], rules, '0')
    return x(sequences[0], rules['0'], rules)


if __name__ == "__main__":
    print(run(read_input('test.txt')))


# def test_input():
#     assert run(read_input('input.txt')) == False
