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


class Allocator:
    pass
