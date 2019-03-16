import pytest
from multiprocessing import Process, Queue

from allocation.allocating import WeightedMap, Allocator


def test_real_case_with_five_objects():
    weights = WeightedMap([
        {'from': '6', 'to': '5', 'weight': 2.0},
        {'from': '6', 'to': '11', 'weight': 6.0},
        {'from': '6', 'to': '25', 'weight': 0.0},
        {'from': '6', 'to': '67', 'weight': 0.0},
        {'from': '6', 'to': '97', 'weight': 4.0},
        {'from': '1', 'to': '5', 'weight': 2.0},
        {'from': '14', 'to': '5', 'weight': 1.0},
        {'from': '20', 'to': '5', 'weight': 3.0},
        {'from': '26', 'to': '5', 'weight': 4.0},
        {'from': '1', 'to': '11', 'weight': 6.0},
        {'from': '14', 'to': '11', 'weight': 3.0},
        {'from': '20', 'to': '11', 'weight': 4.0},
        {'from': '26', 'to': '11', 'weight': 5.0},
        {'from': '1', 'to': '25', 'weight': 0.0},
        {'from': '14', 'to': '25', 'weight': 1.0},
        {'from': '20', 'to': '25', 'weight': 0.0},
        {'from': '26', 'to': '25', 'weight': 1.0},
        {'from': '1', 'to': '67', 'weight': 0.0},
        {'from': '14', 'to': '67', 'weight': 1.0},
        {'from': '20', 'to': '67', 'weight': 2.0},
        {'from': '26', 'to': '67', 'weight': 3.0},
        {'from': '1', 'to': '97', 'weight': 4.0},
        {'from': '14', 'to': '97', 'weight': 5.0},
        {'from': '20', 'to': '97', 'weight': 3.0},
        {'from': '26', 'to': '97', 'weight': 2.0}])

    sources = {w['from']: 1 for w in weights}
    targets = {w['to']: 1 for w in weights}

    allocator = Allocator(sources, weights, targets)
    allocation = allocator.get_best()
    assert len(allocation) == 5

    # now "remove" one target
    targets['97'] = 0
    allocator = Allocator(sources, weights, targets)
    allocation = allocator.get_best()
    assert len(allocation) == 4


def get_allocation(queue, allocator):
    allocation = allocator.get_best()
    queue.put(allocation)


def test_real_case_floating_point():
    # In this test, if limit_denominator is not set, the method
    # allocator.get_best does not finish. This is because of the following
    # nasty floating point rounding problem:

    # In [51]: a, b, c = 0.5, 2/7, 1/14
    # In [52]: (a - c) + (c - b) + (b - a) > 0
    # Out[52]: True

    weights = WeightedMap([
        {'from': 'a', 'to': '1', 'weight': 1/14},
        {'from': 'a', 'to': '2', 'weight': 2/7},
        {'from': 'a', 'to': '3', 'weight': 0.5},
        {'from': 'b', 'to': '1', 'weight': 1/14},
        {'from': 'b', 'to': '2', 'weight': 2/7},
        {'from': 'b', 'to': '3', 'weight': 0.5},
        {'from': 'c', 'to': '1', 'weight': 1/14},
        {'from': 'c', 'to': '2', 'weight': 2/7},
        {'from': 'c', 'to': '3', 'weight': 0.5},
    ])

    sources = {w['from']: 1 for w in weights}
    targets = {w['to']: 1 for w in weights}

    allocator = Allocator(sources, weights, targets, limit_denominator=1000)

    queue = Queue()
    process = Process(target=get_allocation, args=(queue, allocator))
    process.start()
    process.join(3)
    if process.is_alive():
        process.terminate()
        raise AssertionError('computation did not finish in time')

    allocation = queue.get()
    assert len(allocation) == 3
