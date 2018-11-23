class WeightedMap:
    
    def __init__(self, source, target, wmap):
        self.source = source
        self.target = target
        self.wmap = wmap

    @classmethod
    def from_list(cls, the_list):
        source = {a['from'] for a in the_list}
        target = {a['to'] for a in the_list}
        return cls(source, target, the_list)

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_map(self):
        return self.wmap


class Allocation(list):

    def __getitem__(self, i):
        return {a[1] for a in self if a[0] == i}

    @classmethod
    def start_allocation(cls, instances, needs):
        first = [ (None, t) for t, k in needs.items() for i in range(k) ]
        second = [ (s, None) for s, k in instances.items() for i in range(k) ]
        return cls(first + second)



class Needs(dict):
    pass


class Instances(dict):
    pass


class Allocator:
    pass
