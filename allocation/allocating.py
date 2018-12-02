from typing import NewType, Sequence, Mapping

SourceObject = NewType('SourceObject', str)
TargetObject = NewType('TargetObject', str)


class WeightedMap(list):

    def __getitem__(self, key):

        if isinstance(key, str) or key is None:
            return [ stw for stw in self if stw['from'] == key ]

        elif isinstance(key, tuple):
            source, target = key
            for stw in self:
                if stw['from'] == source and stw['to'] == target:
                    return stw['weight']
            return None

        raise ValueError(f"Can't get item, argument must be str, None or tuple, got {key}")
    

class Source:

    def __init__(self, wmap: WeightedMap, instances: Mapping[SourceObject, int]):
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

    def get_weight(self, allocation):
        return sum(self[s, t] for s, t in allocation)


class Target:

    def __init__(self, capacities: Mapping[TargetObject, int]):
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


class Distances(dict):
    pass


class Allocator:

    def __init__(self,
                 sources: Mapping[SourceObject, int],
                 wmap: WeightedMap,
                 targets: Mapping[TargetObject, int]):

        sources_total_qty = sum(sources.values())
        targets_total_qty = sum(targets.values())

        max_val = max(m['weight'] for m in wmap)
        for t in targets.keys():
            wmap.append({'from': None, 'to': t, 'weight': max_val + 1})
        for s in sources.keys():
            wmap.append({'from': s, 'to': None, 'weight': max_val + 1})
        wmap.append({'from': None, 'to': None, 'weight': -1})

        targets[None] = sources_total_qty
        sources[None] = targets_total_qty

        self.sources = Source(wmap, sources)
        self.targets = Target(targets)

    def init_allocation(self) -> Allocation:
        first = [ (s, None) for s, k in self.sources.instances.items() for i in range(k) if s is not None ]
        second = [ (None, t) for t, k in self.targets.capacities.items() for i in range(k) if t is not None ]
        return Allocation(first + second)

    def get_differences(self, allocation: Allocation):
        inf = float('inf')

        differences = dict()
        targets_coll = self.targets.collection
        for t1 in targets_coll:
            for t2 in targets_coll:
                differences[(t1, t2)] = {'path': [], 'diff': inf}

        # first differences
        for source, target_0 in allocation:
            sweights = self.sources.wmap[source]
            current_weight = [sw['weight'] for sw in sweights if sw['to'] == target_0][0]  # TODO: make this prettier

            for stw in sweights:
                target, weight = stw['to'], stw['weight']
                diff = weight - current_weight
                if diff < differences[(target_0, target)]['diff']:
                    differences[(target_0, target)] = {'path': [{'object': stw['from'], 'to': target}], 'diff': diff}

        # now, do Floyd - Warshall
        for middle in targets_coll:
            for first in targets_coll:
                for last in targets_coll:
                    diff_through = differences[(first, middle)]['diff'] + differences[(middle, last)]['diff']
                    if diff_through < differences[(first, last)]['diff']:
                        first_path = differences[(first, middle)]['path']
                        last_path = differences[(middle, last)]['path']
                        differences[(first, last)] = {'path': first_path + last_path, 'diff': diff_through}
        return differences

    def has_cycle(self, differences):
        return any(differences[s, s]['diff'] < 0 for s in self.targets.collection)



