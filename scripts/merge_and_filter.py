#! /usr/bin/env python3

import argparse
import collections
import os
import re
import sys

from pathlib import Path
from xopen import xopen
from pprint import pprint

KEEP = 100

"""
For every read we want to know top 100 matches
"""


class Read:
    """A simple optimized buffer for top matches for a single read.
    """
    def __init__(self, keep):
        self._min_kmers_filter=0 #should be increased once the number of records >keep

    def add_rec(self, batch, sample, kmers):
        self._matches.append( (batch, sample, kmers) )

    def _sort_and_prune(self):
        #1. sort
        self.list.sort(key=lambda x: (x[2], x[0], x[1])) # todo: function
        #2. identify where to stop
        #3. trim the list
        #4. update _min_kmers_filter according to this value

##
## TODO: add support for empty matches / NA values
##
class BestMatches:
    def __init__(self, keep):
        self._keep = keep
        self._read_dict=collections.OrderedDict(lambda: Read(keep=self._keep))

    def _add_rec(batch, sample, read, kmers):
        self._read_dict[read].add_rec(batch, sample, kmers)

    def process_file(self, fn):
        with xopen(fn) as fo:
            print(f"Processing {fn}", file=sys.stderr)
            batch,_,_=Path(fn).name.partition("____")
            #print(batch)
            for x in fo:
                sample, read, kmers=x.strip().split()
                self._add_rec(batch, sample, read, kmers)


    def print_output(self):
        pass


def merge_and_filter(fns, keep):
    bm = BestMatches(keep)
    for fn in fns:
        bm.process_file(fn)
    bm.print_output()


def main():

    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'match_fn',
        metavar='',
        nargs='+',
        help='',
    )

    parser.add_argument(
        '-k',
        metavar='int',
        dest='keep',
        default=KEEP,
        help=f'no. of best hits to keep [{KEEP}]',
    )

    args = parser.parse_args()

    merge_and_filter(args.match_fn, args.keep)


if __name__ == "__main__":
    main()
