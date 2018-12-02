import pytest

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
