import pytest
import random
import time
from multiprocessing import Process, Queue


from allocation import allocating

'''
Case 1:
Source: 0,..., N
Target: 0,..., N
WeightedMap: n --> n   (weight 0)
             n --> n+1 (weight 1)
             n --> n-1 (weight 1)

Case 2:
Source: 0,..., N
Target: 0,..., N
WeightedMap: n --> n   (weight 1)
             n --> n+1 (weight 0 if n is even, 3 if n is odd)
             n --> n-1 (weight 2)
'''


@pytest.fixture
def large_one_to_one():
    elements = range(20)
    sources = {str(e): 1 for e in elements}
    targets = {str(e): 1 for e in elements}
    wmap_list = []
    for e in elements:
        wmap_list.append({'from': str(e), 'to': str(e), 'weight': 0})
        wmap_list.append({'from': str(e), 'to': str((e + 1) % len(elements)), 'weight': 1})
        wmap_list.append({'from': str(e), 'to': str((e - 1) % len(elements)), 'weight': 1})
    wmap = allocating.WeightedMap(wmap_list)

    yield allocating.Allocator(sources, wmap, targets)


@pytest.fixture
def large_one_to_one_alternate():
    elements = range(20)
    sources = {str(e): 1 for e in elements}
    targets = {str(e): 1 for e in elements}
    wmap_list = []
    for e in elements:
        wmap_list.append({'from': str(e), 'to': str(e), 'weight': 1})
        wmap_list.append({'from': str(e), 'to': str((e + 1) % len(elements)), 'weight': 3 * (e % 2)})
        wmap_list.append({'from': str(e), 'to': str((e - 1) % len(elements)), 'weight': 2.5})
    wmap = allocating.WeightedMap(wmap_list)

    yield allocating.Allocator(sources, wmap, targets)


def test_finishes(large_one_to_one):
    allocation = large_one_to_one.get_best()
    for e in large_one_to_one.sources.collection:
        if e is not None:
            assert allocation[e] == {str(e)}


def test_finishes_alternate(large_one_to_one_alternate):
    allocation = large_one_to_one_alternate.get_best()
    for e in large_one_to_one_alternate.sources.collection:
        if e is not None:
            assert allocation[e] == {str(e)}


def large_random(sources_number, targets_number, choices, limit_denominator):
    sources = {str(s): 1 for s in range(sources_number)}
    targets = {str(t): 1 for t in range(targets_number)}

    wmap_list = []
    rnd_weight = lambda: random.uniform(0, 1)
    for source in sources:
        stargets = set(random.choices(list(targets), k=choices))
        for t in stargets:
            wmap_list.append({'from': source, 'to': t,
                              'weight': rnd_weight()})
    wmap = allocating.WeightedMap(wmap_list)

    return allocating.Allocator(sources, wmap, targets, limit_denominator)


testdata = [
    (40, 50, 5, 0, 15),
    (40, 50, 5, 100, 25),
    (60, 70, 5, 0, 15),
    (50, 100, 5, 0, 45),
]


@pytest.mark.parametrize('sources_number,targets_number,choices,limit_denominator,expected_time', testdata)
def test_finishes_random(sources_number, targets_number, choices, limit_denominator, expected_time):
    random.seed(1234)
    allocator = large_random(sources_number, targets_number, choices, limit_denominator)

    def do_alloc(queue):
        allocation = allocator.get_best()
        queue.put(allocation)

    queue = Queue()
    process = Process(target=do_alloc, args=(queue,))
    start = time.monotonic()
    process.start()
    process.join(expected_time * 2)

    if process.is_alive():
        process.terminate()
        raise AssertionError((f'random case with {sources_number} sources, {targets_number} targets, '
                              f'{choices} choices and {limit_denominator} limit_denominator '
                              f'took more than {expected_time * 2} seconds to finish'))
    else:
        print(f'allocation took {time.monotonic() - start:.3f} seconds')

    assert len(queue.get()) >= min(sources_number, targets_number) / 2
