#!/usr/bin/env python3
#===============================================================================
# pileups_merge.py
#===============================================================================

"""Merge pileup files"""




# Imports ======================================================================

import argparse
from pileups.pileups import merge




# Functions ====================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(description='Merge pileup files')
    parser.add_argument('pileup', nargs='+', help='Paths to pileup files')
    parser.add_argument(
        '--alleles',
        action='store_true',
        help='Print pileup alleles and quality scores'
    )
    parser.add_argument(
        '--count',
        action='store_true',
        help='Print reference allele counts'
    )
    parser.add_argument(
        '--reference',
        action='store_true',
        help='Print reference alleles'
    )
    parser.add_argument('--header', help='Add a header to the output')
    parser.add_argument(
        '--het-filter',
        metavar='<int>',
        type=int,
        help='apply het filter'
    )
    args = parser.parse_args()
    if not args.count:
        args.alleles = True
    if args.alleles:
        args.reference = True
    return args


def main():
    args = parse_arguments()
    for row in merge(
        *args.pileup,
        alleles=args.alleles,
        count=args.count,
        reference=args.reference,
        header=(args.header.split() if args.header else None),
        het_filter=args.het_filter
    ):
        print('\t'.join(row), end='\n')
