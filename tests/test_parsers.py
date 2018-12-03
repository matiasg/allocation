from pathlib import Path
import pytest

from allocation.main import load_yaml


def test_load_yaml():
    path = Path(__file__).parent / 'example.yml'
    allocator = load_yaml(path)
    allocation = allocator.get_best()
    assert allocation['a'] == {0, 1}
    assert allocation['b'] == {0}
