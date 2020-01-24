#!/usr/bin/env python3
#===============================================================================
# allelecounts.py
#===============================================================================

"""Functions for handling allele count data"""




# Imports ======================================================================

import os.path
import socket
import sys
import funcgenom




# Functions ====================================================================

def construct_dict(genome, *dataset_names):
    """
    Construct an allele counts dict from a genome object

    Parameters
    ----------
    genome : funcgenom.Genome()
        a genome as from funcgenom
    *dataset_names : str
        names for the datasets represented by the genome
    
    Returns
    -------
    dict
        a dictionary whose values are tables containing the coordinates and
        allele counts
    """

    return {
        'coordinates': dict(
            zip(
                ('chr', 'pos'),
                (
                    list(z) for z in zip(
                        *((v.chromosome, v.position) for v in genome.variants())
                    )
                )
            )
        ),
        **{
            dataset_name: dict(
                zip(
                    ('coverage', 'ref_count'),
                    (
                        list(z) for z in zip(
                            *(
                                (
                                    v.traits.get(dataset_name, {}).get(
                                        'coverage'
                                    ),
                                    v.traits.get(dataset_name, {}).get(
                                        'ref_count'
                                    )
                                )
                                for v in genome.variants()
                            )
                        )
                    )
                )
            )
            for dataset_name in dataset_names
        }
    }


def join_as_dict(
    *counts_file_paths,
    names=None,
    coverage_index=2,
    ref_count_index=3,
    **kwargs
):
    """
    Read allele counts files and join them as a dictionary

    Parameters
    ----------
    counts_file_paths : str
        paths to allele counts files
    dataset_names : iterable
        names corresponding to counts file paths
    coverage_index : int
        column index for coverage in counts files
    ref_count_index : int
        column index for ref count in counts files
    **kwargs
        other parameters for `Genome.load_variants`
    
    Returns
    -------
    dict
        a dictionary whose values are tables containing the coordinates and
        allele counts
    """
    names = names if names else tuple(
        os.path.basename(path).replace('.pileup', '')
        for path in counts_file_paths
    )
    genome = funcgenom.Genome()
    for counts_file_path, name in zip(counts_file_paths, names):
        genome.load_variants(
            counts_file_path,
            traits={
                name: {
                    'coverage': coverage_index,
                    'ref_count': ref_count_index
                }
            },
            **kwargs
        )
        genome.sort_variants()
        genome.resolve_duplicate_variants()
    return construct_dict(genome, *names)
