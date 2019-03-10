import pytest

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
