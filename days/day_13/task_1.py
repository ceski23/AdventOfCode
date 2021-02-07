from helpers import read_input


def find_nearest(buses, time):
    memo = {}
    for bus in buses:
        departure = (time // bus) * bus
        while departure < time:
            departure += bus
        memo[departure] = bus
    nearest_departure = min(memo)
    return nearest_departure, memo[nearest_departure]


def run(data):
    start_time = int(data[0])
    buses_data = data[1].split(',')
    buses = [int(n) for n in filter(lambda x: x != 'x', buses_data)]

    departure_time, bus = find_nearest(buses, start_time)
    return bus * (departure_time - start_time)


if __name__ == "__main__":
    print(run(read_input('input.txt')))


def test_input():
    assert run(read_input('input.txt')) == 3865


def test_test():
    assert run(read_input('test.txt')) == 295
