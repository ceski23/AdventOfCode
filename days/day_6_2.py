def countGroup(group):
    yes = None
    for questions in group:
        if yes != None:
            yes = yes.intersection(set(questions))
        else:
            yes = set(questions)
    return len(yes)


def run():
    with open('inputs/6.txt') as f:
        group = []
        count = 0
        for line in f:
            if len(line.strip()) > 0:
                group.append(line.strip())
            else:
                count += countGroup(group)
                group = []
        count += countGroup(group)
        return count


if __name__ == "__main__":
    print(run())
