import pytest

from allocation import allocating

@pytest.fixture
def small_wmap():
    the_list = [
            {'from': 'a', 'to': 0, 'weight': 1},
            {'from': 'a', 'to': 1, 'weight': 0},
            {'from': 'b', 'to': 0, 'weight': 2}
            ]
    yield the_list

@pytest.fixture
def small_allocation():
    yield [ ('a', 0), ('a', 1), ('b', 0) ]


@pytest.fixture
def small_needs():
    yield { 0: 3, 1: 1 }


@pytest.fixture
def small_instances():
    yield { 'a': 2, 'b': 1 }


def test_wmap_instance_from_list(small_wmap):
    wmap = allocating.WeightedMap.from_list(small_wmap)
    assert len(wmap.get_source()) == 2
    assert len(wmap.get_target()) == 2
    assert len(wmap.get_map()) == 3


def test_allocation(small_allocation):
    a = allocating.Allocation(small_allocation)
    assert len(a) == 3
    assert a['a'] == {0, 1}
    assert a['b'] == {0}


def test_needs(small_needs):
    n = allocating.Needs(small_needs)
    assert n[0] == 3
    assert n[1] == 1


def test_instances(small_instances):
    i = allocating.Instances(small_instances)
    assert i['a'] == 2
    assert i['b'] == 1


def test_start_allocation(small_instances, small_needs):
    a = allocating.Allocation.start_allocation(small_instances, small_needs)
    assert a['a'] == {None}
    assert a['b'] == {None}
    assert a[None] == {0, 1}
