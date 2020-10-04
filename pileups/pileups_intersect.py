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
        help='paths to pileup files'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    for row in intersect(*args.file_paths):
        print('\t'.join(str(item) for item in row))
