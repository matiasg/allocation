import pytest

from allocation import allocating

'''
small case is given by

Source: a, a, b (two copies of a)
Target: 0, 0, 0, 1 (0 has capacity == 3)
WeightedMap: a --> 0 (weight 1)
             a --> 1 (weight 0)
             b --> 0 (weight 0)

The best allocation is:
            0: {a, b}
            1: {a}

small case 2:
    Source: a, a, b
    Target: 0, 0, 1
    WeightedMap: a --> 0 (weight 0)
                 a --> 1 (weight 1)
                 b --> 0 (weight 1)
                 b --> 1 (weight 0)
    Best allocation:
                0: {a, b}
                1: {a}
    This is because we do not allow 0: {a, a}
    (which would clearly be the same as 0: {a} )
'''


@pytest.fixture
def small_wmap():
    the_list = [
            {'from': 'a', 'to': 0, 'weight': 1},
            {'from': 'a', 'to': 1, 'weight': 0},
            {'from': 'b', 'to': 0, 'weight': 2}
            ]
    yield allocating.WeightedMap(the_list)


@pytest.fixture
def small_allocation():
    yield [('a', 0), ('a', 1), ('b', 0)]


@pytest.fixture
def small_target():
    yield {0: 3, 1: 1}


@pytest.fixture
def small_instances():
    yield {'a': 2, 'b': 1}


@pytest.fixture
def small_source(small_wmap, small_instances):
    yield allocating.Source(small_wmap, small_instances)


@pytest.fixture
def small_allocator(small_instances, small_wmap, small_target):
    allocator = allocating.Allocator(small_instances, small_wmap, small_target)
    yield allocator


@pytest.fixture
def small_source(small_wmap, small_instances):
    yield allocating.Source(small_wmap, small_instances)


@pytest.fixture
def small_allocator(small_instances, small_wmap, small_target):
    allocator = allocating.Allocator(small_instances, small_wmap, small_target)
    yield allocator


def test_allocation(small_allocation):
    a = allocating.Allocation(small_allocation)
    assert len(a) == 3
    assert a['a'] == {0, 1}
    assert a['b'] == {0}


def test_target(small_target):
    n = allocating.Target(small_target)
    assert n[0] == 3
    assert n[1] == 1


def test_source(small_source):
    assert small_source['a'] == 2
    assert small_source['b'] == 1
    assert small_source[('a', 0)] == 1
    assert small_source[('a', 2)] is None


def test_start_allocation(small_allocator):
    allocation = small_allocator.init_allocation()
    assert allocation['a'] == {None}
    assert allocation['b'] == {None}
    assert allocation[None] == {0, 1}
    with pytest.raises(KeyError):
        allocation['c']


def test_wmap(small_allocator):
    wmap = small_allocator.sources.wmap
    assert any(ftw['from'] == 'a' and ftw['to'] == 0 for ftw in wmap)
    assert any(ftw['from'] == 'a' and ftw['to'] == 1 for ftw in wmap)
    assert any(ftw['from'] == 'a' and ftw['to'] is None for ftw in wmap)
    assert any(ftw['from'] is None and ftw['to'] == 0 for ftw in wmap)
    assert any(ftw['from'] is None and ftw['to'] is None for ftw in wmap)


def test_init_allocation_weight(small_allocator):
    sources = small_allocator.sources
    allocation = small_allocator.init_allocation()
    assert sources.get_weight(allocation) > 1


def test_allocator_rotate(small_allocator):
    allocation = small_allocator.init_allocation()
    path = [{'object': None, 'to': None}, {'object': 'a', 'to': 1}, {'object': None, 'to': 0}]
    small_allocator.rotate(allocation, path)
    assert allocation[None] == {0, None}
    assert allocation['a'] == {1, None}
    assert allocation['b'] == {None}


def test_allocator(small_allocator):
    allocation = small_allocator.get_best()
    assert allocation['a'] == {0, 1}
    assert allocation['b'] == {0}


@pytest.fixture
def small_allocator_2():
    the_list = [
            {'from': 'a', 'to': 0, 'weight': 0},
            {'from': 'a', 'to': 1, 'weight': 1},
            {'from': 'b', 'to': 0, 'weight': 1},
            {'from': 'b', 'to': 1, 'weight': 0}
            ]
    wmap = allocating.WeightedMap(the_list)
    instances = {'a': 2, 'b': 1}
    capacities = {0: 2, 1: 1}
    yield allocating.Allocator(instances, wmap, capacities)


def test_allocator_2(small_allocator_2):
    allocation = small_allocator_2.get_best()
    assert allocation['a'] == {0, 1}
    assert allocation['b'] == {0}
