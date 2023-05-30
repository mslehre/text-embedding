#!/usr/bin/env python3

import os
import argparse
import numpy as np
import h5py
from compute_embedding import embedding_from_string


def read_pubs_to_dict():
    """
    """
    pubs = {}
    affiliation = []  # save author faculty institute
    return pubs, affiliation


def embeddings_from_pubs(pubs: dict, 
                         embedding_name: 'text-embedding-ada-002',
                         max_token: 8191) -> np.ndarray:
    
    """
    Get the embeddings of the publications for every author

    Args:
        pubs (dict):
        embedding_name (str): The name of the embedding model. By default the
            model text-embedding-ada-002 is used.
        max_token (int): The maximum number of tokens for which an embedding is
            computed. By default this is the maximum number of tokens of the 
            embedding model text-embedding-ada-002.
        
    Returns:
        embeddings (np.ndarray): Embeddings of the publication lists.
    """

    embeddings = []  

    for author in pubs:
        embeddings.append(embedding_from_string(pubs[author],
                                              embedding_name = embedding_name,
                                              max_token = max_token))
    embeddings = np.asarray(embeddings, dtype=np.float64)

    if np.isnan(embeddings).any():  # check if all embeddings were computed
        print("WARNING: At least one embedding wasn't computed! Please check " 
              + "your input and parameters!")
        exit(1)

    return embeddings


def main():
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('input', help = '')
    parser.add_argument('-o', '-outfile', default = 'pub_embed',
                        help = 'Stem for output file.')
    parser.add_argument('--descr', type = str, 
                        help = 'Custom description for hdf5 file')
    args = parser.parse_args()

    # test if input is readable

    outfile = args.outfile + ".hdf5"
    # description for datasets
    descr = "" if not args.descr else args.descr  #### write description

    # read data and compute embeddings
    pubs, affiliation = read_pubs_to_dict(args.input)
    embeddings = embeddings_from_pubs(pubs)

    # write embeddings and author affiliations to hdf5 file
    with h5py.File(outfile, 'w') as f_out:
        f_out.create_dataset(name = 'pub_embedding', data = embeddings,
                             dtype = 'f', compression = 'gzip')
        
        f_out.create_dataset(name = 'author_affiliation', data = affiliation,
                             comperession = 'gzip')
        
        f_out.create_dataset('description', 
                             data = descr)  
    
    exit(0)


if __name__ == "__main__":
    main()