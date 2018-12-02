from typing import NewType, Sequence, Mapping, Optional, Dict, List, Tuple
from mypy_extensions import TypedDict

SourceObject = NewType('SourceObject', str)
TargetObject = NewType('TargetObject', str)

Switch = TypedDict('Switch', {'object': Optional[SourceObject], 'to': Optional[TargetObject]})
Path = List[Switch]
DiffPath = TypedDict('DiffPath', {'diff': float, 'path': Path})
Differences = Dict[Tuple[Optional[TargetObject], Optional[TargetObject]], DiffPath]

WeightedNode = TypedDict('WeightedNode', {'from': Optional[SourceObject],
                                          'to': Optional[TargetObject],
                                          'weight': float})


class WeightedMap(list):

    def __init__(self, nodes: Sequence[WeightedNode]):
        super().__init__(nodes)

    def __getitem__(self, key):

        if isinstance(key, str) or key is None:
            return [stw for stw in self if stw['from'] == key]

        elif isinstance(key, tuple):
            source, target = key
            for stw in self:
                if stw['from'] == source and stw['to'] == target:
                    return stw['weight']
            return None

        raise ValueError(f"Can't get item, argument must be str, None or tuple. Got {key}")


class Source:

    def __init__(self, wmap: WeightedMap, instances: Mapping[Optional[SourceObject], int]):
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

    def get_weight(self, allocation) -> float:
        return sum(self[s, t] for s, t in allocation)


class Target:

    def __init__(self, capacities: Mapping[Optional[TargetObject], int]):
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


class Allocator:

    def __init__(self,
                 sources: Dict[Optional[SourceObject], int],
                 wmap: WeightedMap,
                 targets: Dict[Optional[TargetObject], int]):

        sources_total_qty = sum(sources.values())
        targets_total_qty = sum(targets.values())

        max_val = max(m['weight'] for m in wmap)
        for t in targets.keys():
            wmap.append({'from': None, 'to': t, 'weight': max_val + 1})
        for s in sources.keys():
            wmap.append({'from': s, 'to': None, 'weight': max_val + 1})
        wmap.append({'from': None, 'to': None, 'weight': -1})

        sources[None] = targets_total_qty
        targets[None] = sources_total_qty

        self.sources = Source(wmap, sources)
        self.targets = Target(targets)

    def init_allocation(self) -> Allocation:
        first: List[Tuple[Optional[SourceObject], Optional[TargetObject]]]
        second: List[Tuple[Optional[SourceObject], Optional[TargetObject]]]
        first = [(s, None) for s, k in self.sources.instances.items() for i in range(k) if s is not None]
        second = [(None, t) for t, k in self.targets.capacities.items() for i in range(k) if t is not None]
        return Allocation(first + second)

    def get_differences(self, allocation: Allocation) -> Differences:
        inf = float('inf')

        differences: Differences = dict()
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

    def has_cycle(self, differences: Differences) -> bool:
        return self.get_cycle(differences) is not None

    def get_cycle(self, differences: Differences) -> Optional[DiffPath]:
        for t in self.targets.collection:
            pd = differences[(t, t)]
            if pd['diff'] < 0:
                return pd
        return None

    def rotate(self, allocation: Allocation, path: Path) -> None:
        s = path[-1]['to']
        for ot in path:
            t = ot['to']
            o = ot['object']
            # must move o from s to t
            idx = allocation.index((o, s))
            allocation.pop(idx)
            allocation.append((o, t))
            s = t

    def get_best(self) -> Allocation:
        allocation = self.init_allocation()
        differences = self.get_differences(allocation)
        cycle = self.get_cycle(differences)

        while cycle is not None:
            self.rotate(allocation, cycle['path'])
            differences = self.get_differences(allocation)
            cycle = self.get_cycle(differences)

        return allocation
