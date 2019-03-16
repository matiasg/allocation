import pytest

from allocation.allocating import Allocation


def test_Allocation():
    allocation = Allocation([('a', '1'), ('b', '2'), (None, '3'), ('c', None)])
    assert len(allocation) == 2
