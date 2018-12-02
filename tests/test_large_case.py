import pytest

from allocation import allocating

'''
Source: 0,..., 50
Target: 0,..., 50
WeightedMap: n --> n   (weight 0)
             n --> n+1 (weight 1)
             n --> n-1 (weight 1)
'''

@pytest.fixture
def large_one_to_one():
    elements = range(50)
    sources = {str(e): 1 for e in elements}
    targets = {str(e): 1 for e in elements}
    wmap_list = []
    for e in elements:
        wmap_list.append({'from': str(e), 'to': str(e), 'weight': 0})
        wmap_list.append({'from': str(e), 'to': str((e + 1) % len(elements)), 'weight': 1})
        wmap_list.append({'from': str(e), 'to': str((e - 1) % len(elements)), 'weight': 1})
    wmap = allocating.WeightedMap(wmap_list)

    yield allocating.Allocator(sources, wmap, targets)

def test_finishes(large_one_to_one):
    allocation = large_one_to_one.get_best()
    for e in large_one_to_one.sources.collection:
        if e is not None:
            assert allocation[e] == {str(e)}
