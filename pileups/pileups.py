#!/usr/bin/env python3
#===============================================================================
# pileups.py
#===============================================================================

# Imports ======================================================================

import argparse
import socket
import sys
import funcgenom




# Functions ====================================================================

def generate_counts(iterable, mode='cr', header=False):
    """Generate allele counts from a pileup file
    
    Parameters
    ----------
    iterable : iterable
        An iterable.
    mode : str
        Mode for producing allele counts. This should be a string of characters
        chosen from "a", "c", and/or "r". It defines which counts are included
        and in what order - e.g. "cr" means "coverage and ref count", while
        "cra" means "coverage, ref count, and alt count."
    header : bool
        If True, yield a header first.
    
    Yields
    ------
    tuple
        A row containing chromosome, position, and counts
    """

    if not set(mode) <= {'a', 'c', 'r'}:
        raise Exception('mode arg must include only "a", "c", and/or "r".')
    if header:
        header_dict = {'a': 'alt_count', 'c': 'coverage', 'r': 'ref_count'}
        yield ('chr', 'pos') + tuple(header_dict[m] for m in mode)
    for item in iterable:
        chromosome, position, _, coverage, read_bases, _ = (
            item.split() if isinstance(item, str) else item
        )
        ref_count = read_bases.replace(',', '.').count('.')
        count_dict = {
            'a': int(coverage) - ref_count,
            'c': int(coverage),
            'r': ref_count
        }
        yield (chromosome, int(position)) + tuple(count_dict[m] for m in mode)


def count_ref_alleles(variant, *traits):
    """Count reference allels for a variant
    
    Parameters
    ----------
    variant : a Variant as from funcgenom
        the variant for which alleles should be counted
    *traits : str
        the traits for which alleles should be counted
    

    Returns
    -------
    int
        the reference allele count
    """

    return (
        ''.join(variant.traits[trait]['alleles'] for trait in traits)
        .replace(',', '.')
        .count('.')
    )


def merge(*file_paths, alleles=True, count=False, reference=True, header=None):

    """Merge a group of pileup files on disk into a single pileup
    
    Parameters
    ----------
    *file_paths : str
        paths to pileup files
    alleles : bool
        include raw alleles in output if True
    count : bool
        include reference allele count in output if True
    reference : bool
        include reference allele in output if True
    header : iterable
        provide a header for the output
    
    Yields
    -------
    tuple
        a row of the merged pileup file
    """

    genome = funcgenom.Genome()
    for file_path in file_paths:
        genome.load_variants(
            file_path,
            add_header=('chr', 'pos', 'ref', 'coverage', 'alleles', 'qual'),
            traits={
                file_paths.index(file_path):
                    {'ref': 2, 'coverage': 3, 'alleles': 4, 'qual': 5}
            }
        )
        genome.sort_variants()
        genome.resolve_duplicate_variants()
    if header:
        yield header
    for variant in genome.variants():
        indices = tuple(variant.traits.keys())
        yield (
            ('chr{}'.format(variant.chromosome), str(variant.position))
            + reference * (variant.traits[indices[0]]['ref'].casefold(),)
            + (str(int(sum(variant.traits[i]['coverage'] for i in indices))),)
            + alleles * (
                ''.join(variant.traits[i]['alleles'] for i in indices),
                ''.join(str(variant.traits[i]['qual']) for i in indices)
            )
            + count * (str(count_ref_alleles(variant, *indices)),)
        )
