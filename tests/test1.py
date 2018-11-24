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
def small_target():
    yield { 0: 3, 1: 1 }


@pytest.fixture
def small_instances():
    yield { 'a': 2, 'b': 1 }


def test_allocation(small_allocation):
    a = allocating.Allocation(small_allocation)
    assert len(a) == 3
    assert a['a'] == {0, 1}
    assert a['b'] == {0}


def test_target(small_target):
    n = allocating.Target(small_target)
    assert n[0] == 3
    assert n[1] == 1


def test_source(small_wmap, small_instances):
    i = allocating.Source(small_wmap, small_instances)
    assert i['a'] == 2
    assert i['b'] == 1
    assert i[('a', 0)] == 1
    assert i[('a', 2)] is None


def test_start_allocation(small_wmap, small_instances, small_target):
    source = allocating.Source(small_wmap, small_instances)
    target = allocating.Target(small_target)
    allocation = allocating.Allocation.start_allocation(source, target)
    assert allocation['a'] == {None}
    assert allocation['b'] == {None}
    assert allocation[None] == {0, 1}
    with pytest.raises(KeyError):
        allocation['c']
