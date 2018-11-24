class WeightedMap(list):
    pass
    

class Source:

    def __init__(self, wmap: WeightedMap, instances):
        self.collection = {a['from'] for a in wmap}
        self.wmap = wmap
        self.instances = instances

    def __getitem__(self, s):

        if isinstance(s, str):
            return self.instances[s]

        elif isinstance(s, tuple) and len(s) == 2:
            records = [r for r in self.wmap if r['from'] == s[0] and r['to'] == s[1]]
            if not records:
                return None
            # TODO: what if more than one record? Sanitize input
            return records[0]['weight']



class Target:

    def __init__(self, capacities):
        self.collection = capacities.keys()
        self.capacities = capacities

    def __getitem__(self, t):
        return self.capacities[t]


class Allocation(list):

    def __getitem__(self, i):
        result = {a[1] for a in self if a[0] == i}
        if not result:
            raise KeyError(f'No {i} in source')
        return result

    @classmethod
    def start_allocation(cls, source: Source, target: Target):
        first = [ (s, None) for s, k in source.instances.items() for i in range(k) ]
        second = [ (None, t) for t, k in target.capacities.items() for i in range(k) ]
        return cls(first + second)


class Allocator:
    pass
