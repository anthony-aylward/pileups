#!/usr/bin/env python3
#===============================================================================
# pileups_dist.py
#===============================================================================

"""Plot distribution of a pileup"""




# Imports ======================================================================

import argparse
import seaborn as sns

from pileups.pileups import generate_counts




# Functions ====================================================================

def ref_frac_dist(pileup_file_path):
    with open(pileup_file_path, 'r') as f:
        return tuple(r / c for _, _, c, r in generate_counts(f) if c > 0)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="plot the distribution of a pileup"
    )
    parser.add_argument(
        'pileup',
        metavar='<path/to/file.pileup>',
        help='path to pileup'
    )
    parser.add_argument(
        'output',
        metavar='<path/to/output.{pdf,png,svg}>',
        help='path to output file'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    dist = ref_frac_dist(args.pileup)
    ax = sns.distplot(dist)
    fig = ax.get_figure()
    fig.savefig(args.output)
