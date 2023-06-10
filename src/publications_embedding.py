#!/usr/bin/env python3

import os
import argparse
import numpy as np
import h5py
from compute_embedding import embedding_from_string


def try_to_read_dir(dir_path: str) -> str:
    # a quick function for argparse to check if given arg is a readable dir
    if not os.path.isdir(dir_path) or not os.access(dir_path, os.R_OK):
        raise argparse.ArgumentTypeError("The directory " + dir_path + " does "
                                         + "not exist or is not readable!")
    return dir_path

def read_pubs(dir_path: str, 
              n: int) -> tuple[list[str], np.ndarray]:
    """
    Read publication lists in given directory

    Args:
        dir_path (str): Path to directory containing files with publication
            lists. The names of the files are expected to be a subset of 
            {0.txt, ... n-1.txt}. Every one of those files are tried.
        n (int): Number of expected file in the directory.

    Returns:
        pubs (list[str]): List of length n. Every entry contains a string 
            representing a list of publications of an author.
        author_ids (numpy.ndarray): List of author ids corresponding to the 
            publication lists.
    """

    dir_path = os.path.join(dir_path, '')  # append '/' if not already there
    pubs = []
    author_ids = []

    for i in range(n):  # loop over all possible files
        file_path = dir_path + str(i) + ".txt"

        # check if file exists and is readable, if yes open and read
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            author_pubs = []
            author_ids.append(i)  # save ID
            with open(file_path, 'r') as file_handle:
                lines = file_handle.readlines()
                for line in lines[1:]:  # exclude first line containing author
                    if line.strip():  # check if line is not empty
                        # add publication title and ignore link
                        author_pubs.append(line.split('\t')[0])
                author_pubs = "; ".join(author_pubs)
                pubs.append(author_pubs)

    author_ids = np.asarray(author_ids)

    return pubs, author_ids

def embeddings_from_pubs(pubs: list[str], 
                         embedding_name: str = 'text-embedding-ada-002',
                         max_token: int = 8191 ) -> np.ndarray:    
    """
    Get the embeddings of the publications for every author

    Args:
        pubs (list[str]):
        embedding_name (str): The name of the embedding model. By default the
            model text-embedding-ada-002 is used.
        max_token (int): The maximum number of tokens for which an embedding is
            computed. By default this is the maximum number of tokens of the 
            embedding model text-embedding-ada-002.
        
    Returns:
        embeddings (numpy.ndarray): Embeddings of the publication lists.
    """

    embeddings = []

    for pub in pubs:
        embed = embedding_from_string(pub,
                                          embedding_name = embedding_name,
                                          max_token = max_token)
        if embed == [None]:
            print("ERROR: The embedding for \"", pub, "\" could not be" 
                  + "computed! Please check your input and parameters!")
            exit(1)
        embeddings.append(embed)

    embeddings = np.asarray(embeddings)

    return embeddings


def main():
    parser = argparse.ArgumentParser(
        description='Compute embeddings for lists of publications.')
    parser.add_argument('-p', '--publications', type = try_to_read_dir, 
                        required = True,
                        help = 'Directory containing files with names ' 
                        + '<author_id>.txt, which contain publication lists.')
    parser.add_argument('-n', '--num_authors', type = int, required = True,
                        help = 'Number of expected files in the publications ' 
                        + 'directory, i.e. if the highest author ID in the ' 
                        + 'directory is 10, specify 11 as the indexing starts '
                        + 'with 0. All files in {0.txt, ... n-1.txt} are ' 
                        + 'tried, a subset may be missing.')
    parser.add_argument('-o', '--outfile', default = 'pub_embed.h5',
                        help = 'Output file in hdf5 format with data sets: ' 
                        + 'publication_embedding: 2-dim numpy array with '
                        + 'embeddings. author_ids: 1-dim numpy array '
                        + 'containing the ids for each embedding.')
    args = parser.parse_args()        

    # read publications and compute embeddings
    pubs, author_ids = read_pubs(args.publications, args.num_authors)
    embeddings = embeddings_from_pubs(pubs)

    # write data to hdf5 file
    with h5py.File(args.outfile, 'w') as f_out:
        f_out.create_dataset(name = 'publication_embedding', 
                             data = embeddings,
                             compression = 'gzip')
        f_out.create_dataset(name = 'author_ids', 
                             data = author_ids,
                             compression = 'gzip')
    
    exit(0)


if __name__ == "__main__":
    main()
