#!/usr/bin/env python3
#===============================================================================
# pileups_intersect.py
#===============================================================================

"""Intersect a pileup with other pileups"""




# Imports ======================================================================

from argparse import ArgumentParser
from pileups.pileups import intersect




# Functions ====================================================================

def parse_arguments():
    parser = ArgumentParser(description='Intersect a pileup with other pileups')
    parser.add_argument(
        'file_paths',
        metavar='<path/to/file.pileup>',
        nargs='+'
        help='paths to pileup files'
    )
    args = parser.parse_args()
    if len(args.file_paths) < 2:
        raise RuntimeError('please provide at least two arguments')
    return args


def main():
    args = parse_arguments()
    for row in intersect(*args.file_paths):
        print('\t'.join(str(item) for item in row))
