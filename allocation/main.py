from argparse import ArgumentParser
import logging
import yaml

from .allocating import WeightedMap, Allocator, Allocation

logger = logging.getLogger(__name__)


def parse():
    parser = ArgumentParser()
    parser.add_argument('-a', '--allocate', help='yaml file with resources to allocate', required=True)
    parser.add_argument('--out', choices=('empty', 'term'), default='term', help='type of output')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='be (more) verbose')
    args = parser.parse_args()
    return args


def load_yaml(infile) -> Allocator:
    # see https://github.com/yaml/pyyaml/issues/202
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        with open(infile) as yafile:
            y = yaml.load(yafile)

    wmap_list = [{'from': w[0], 'to': w[1], 'weight': w[2]} for w in y['weights']]
    wmap = WeightedMap(wmap_list)

    return Allocator(y['sources'], wmap, y['targets'])



def main(args) -> Allocation:
    allocator = load_yaml(args.allocate)
    allocation = allocator.get_best()
    return allocation
