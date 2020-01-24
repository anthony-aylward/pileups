#!/usr/bin/env python3
#===============================================================================
# pileups_count.py
#===============================================================================

"""Convert mpileup format to allele counts"""




# Imports ======================================================================

import argparse
import json
import os
import socket
import sys
import tempfile

from pileups.pileups import generate_counts
from pileups.allelecounts import join_as_dict





# Functions ====================================================================

def construct_counts_dict(
    pileup_file_path,
    mode='cr',
    header=True,
    temp_dir=None
):
    with tempfile.NamedTemporaryFile(dir=temp_dir) as temp_counts:
        temp_counts_name = temp_counts.name
    with open(pileup_file_path, 'r') as f, open(temp_counts_name, 'w') as g:
        g.write(
            '\n'.join(
                '\t'.join(str(item) for item in row)
                for row in generate_counts(
                    f, mode=mode, header=header
                )
            )
            + '\n'
        )
    counts = join_as_dict(temp_counts_name)
    os.remove(temp_counts_name)
    return counts


def print_tabular(pileup_file_path, mode='cr', header=True):
    with open(pileup_file_path, 'r') as f:
        for row in generate_counts(
            f,
            mode=mode,
            header=header
        ):
            print('\t'.join(str(item) for item in row))


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
        '--json',
        action='store_true',
        help='emit counts in JSON format'
    )
    parser.add_argument(
        '--no-header',
        action='store_true',
        help='do not include a header'
    )
    parser.add_argument(
        '--mode',
        metavar='<mode>',
        default='cr',
        help=(
            'string defining mode for counts, default is coverage and ref '
            'count [cr]'
        )
    )
    parser.add_argument(
        '--tmp-dir',
        metavar='<temp/file/dir/>',
        help='directory for temporary files'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.json:
        print(
            json.dumps(
                construct_counts_dict(
                    args.pileup,
                    mode=args.mode,
                    header=not args.no_header,
                    temp_dir=args.tmp_dir
                )
            )
        )
    else:
        print_tabular(args.pileup, mode=args.mode, header=not args.no_header)
