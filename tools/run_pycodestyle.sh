#!/bin/sh

CONFIG=$(dirname $0)/linting.cfg

python3 -m pycodestyle --config=${CONFIG} allocation
python3 -m pycodestyle --config=${CONFIG} tests

