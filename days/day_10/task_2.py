from helpers import read_input


def build_graph(data):
    adapters = [int(x) for x in data]
    built_in = max(adapters) + 3
    adapters.append(0)
    adapters.append(built_in)
    graph = {}

    for adapter in adapters:
        compatible = filter(lambda x: adapter-3 <= x < adapter, adapters)
        for node in compatible:
            if node not in graph:
                graph[node] = []
            graph[node].append(adapter)
    return graph, built_in


def find(graph, start, end, count=0):
    if start == end:
        return count + 1
    else:
        counts = 0
        for node in graph[start]:
            counts += find(graph, node, end, count)
        print('COUNTS:', counts)
        return counts


def run(data):
    graph, built_in = build_graph(data)
    return find(graph, 0, built_in)


if __name__ == "__main__":
    import time
    start_time = time.time()
    print(run(read_input('input.txt')))
    print("--- %s seconds ---" % (time.time() - start_time))


def test_input():
    # assert run(read_input('input.txt')) ==
    assert 1 == 2


def test_1():
    assert run(read_input('test_1.txt')) == 8


def test_2():
    assert run(read_input('test_2.txt')) == 19208
