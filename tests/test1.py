from allocation import allocating

def test_wmap_instance_from_list():
    the_list = [
            {'from': 'a', 'to': 0, 'weight': 1},
            {'from': 'a', 'to': 1, 'weight': 0},
            {'from': 'b', 'to': 0, 'weight': 2}
            ]
    wmap = allocating.WeightedMap.from_list(the_list)
    assert len(wmap.get_source()) == 2
    assert len(wmap.get_target()) == 2
    assert len(wmap.get_map()) == 3

