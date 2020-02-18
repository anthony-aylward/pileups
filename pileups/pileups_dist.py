#!/usr/bin/env python3
#===============================================================================
# pileups_dist.py
#===============================================================================

"""Plot distribution of a pileup"""




# Imports ======================================================================

import argparse
import seaborn as sns

from statistics import median
from pileups.pileups import generate_counts




# Functions ====================================================================

def ref_frac_dist(pileup_file_path: str, heterozygosity: int = 1):
    with open(pileup_file_path, 'r') as f:
        return tuple(
            r / c for _, _, c, r in generate_counts(f) if all(
                (c > 0, r >= heterozygosity, c - r >= heterozygosity)
            )
        )


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
    parser.add_argument(
        '--heterozygosity',
        metavar='<int>',
        type=int,
        default=1,
        help='heterozygosity threshold'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    dist = ref_frac_dist(args.pileup, heterozygosity=args.heterozygosity)
    ax = sns.distplot(dist)
    ax.axvline(x=median(dist))
    fig = ax.get_figure()
    fig.savefig(args.output)
