import pytest

import os
import random
import time
from multiprocessing import Process, Queue

from allocation import allocating


def large_random(sources_number, targets_number, choices, limit_denominator, wmclass):
    sources = {str(s): 1 for s in range(sources_number)}
    targets = {str(t): 1 for t in range(targets_number)}

    wmap_list = []
    for source in sources:
        stargets = set(random.choices(list(targets), k=choices))
        for t in stargets:
            wmap_list.append({'from': source, 'to': t,
                              'weight': random.uniform(0, 1)})
    wmap = wmclass(wmap_list)

    return allocating.Allocator(sources, wmap, targets, limit_denominator)



if os.environ.get("TEST_TYPE", None) == "performance":
    testdata = [(40, 50, 5, 0, 15),
                (40, 50, 5, 100, 25),
                (60, 70, 5, 0, 15),
                (50, 100, 5, 0, 45)]
else:
    testdata = [(10, 10, 3, 100, 4)]


@pytest.mark.parametrize('sources_number,targets_number,choices,limit_denominator,expected_time', testdata)
@pytest.mark.parametrize('wmclass', [allocating.ListWeightedMap, allocating.DictWeightedMap])
def test_finishes_random(sources_number, targets_number, choices, limit_denominator, expected_time, wmclass):
    random.seed(1234)
    allocator = large_random(sources_number, targets_number, choices, limit_denominator, wmclass)

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
