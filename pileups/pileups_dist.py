#!/usr/bin/env python3
#===============================================================================
# pileups_dist.py
#===============================================================================

"""Plot distribution of a pileup"""




# Imports ======================================================================

import argparse

from pileups.pileups import generate_counts





# Functions ====================================================================

def ref_frac_dist(pileup_file_path):
    with open(pileup_file_path, 'r') as f:
        return tuple(r / c for _, _, c, r in generate_counts(f))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="convert a pileup to allele counts"
    )
    parser.add_argument(
        'pileup',
        metavar='<path/to/file.pileup>',
        help='path to pileup'
    )
    parser.add_argument(
        '--tmp-dir',
        metavar='<temp/file/dir/>',
        help='directory for temporary files'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    dist = ref_frac_dist(args.pileup)
    
