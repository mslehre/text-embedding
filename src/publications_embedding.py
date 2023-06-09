#!/usr/bin/env python3

import os
import argparse
import numpy as np
import h5py
from compute_embedding import embedding_from_string


def dir_readable(arg):
    if not os.path.isdir(arg) or not os.access(arg, os.R_OK):
        raise argparse.ArgumentTypeError("The directory " + arg + " does not "
                                         + "exist or is not readable!")
    return arg

def read_pubs(dir_path: str, 
              n: int) -> tuple(list[str], np.ndarray):
    """
    Read publication lists in given directory

    Args:
        dir_path (str): Path to directory containing files with publication
            lists. 
        n (int): Number of expected file in the directory.

    Returns:
        pubs (list[str]): List of length n. Every entry contains a list of
            publications of an author in a string or None if no file exists for
            the author.
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
            author_pubs = ""
            author_ids.append(i)  # save ID
            with open(file_path, 'r') as file_handle:
                lines = file_handle.readlines()
                for line in lines[1:]:  # exclude first line containing author
                    if line.strip():  # check if line is not empty
                        # add publication title
                        author_pubs += " " + line.split('\t')[0] + ";"
                author_pubs = author_pubs.lstrip()  # remove leading space
                pubs.append(author_pubs)

    author_ids = np.asarray(author_ids)

    return pubs, author_ids

def embeddings_from_pubs(pubs: list[str], 
                         embedding_name: 'text-embedding-ada-002',
                         max_token: 8191 ) -> np.ndarray:    
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

    embedding = []

    for pub in pubs:
        embedding.append(embedding_from_string(pub,
                                               embedding_name = embedding_name,
                                               max_token = max_token))
        if embedding[-1] == None:
            print("ERROR: The embedding for \"", pub, "\" could not be" 
                  + "computed! Please check your input and parameters!")
            exit(1)

    embedding = np.asarray(embedding)

    return embedding


def main():
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('-p', '--publications', type = dir_readable, 
                        required = True,
                        help = 'Directory containing files with names ' 
                        + '<author_id>.txt.')
    parser.add_argument('-n', '--num_authors', type = int, required = True,
                        help = 'Number of expected files in the publications ' 
                        + 'directory, i.e if the highest author id in the ' 
                        + 'directory is 10, specify 11 as the indexing starts '
                        + 'with 0. A subset of the files may be missing.')
    parser.add_argument('-o', '-outfile', default = 'pub_embed.h5',
                        help = 'Output file in hdf5 format.')
    parser.add_argument('--descr', type = str,
                        help = 'Custom description in the hdf5 file.')
    args = parser.parse_args()

    
    descr = args.descr if args.descr else \
        "publication_embedding: 2-dim numpy array\n" \
        + "Each line contains the embedding of a publication list computed " \
        + "with embedding model \"text-embedding-ada-002\".\n\n" \
        + "author_ids: 1-dim numpy array\n" \
        + "Each entry contains the author ID corresponding to the " \
        + "publication list embedding at the same index in " \
        + "publication_embedding."

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
        f_out.create_dataset(name = 'description', 
                             data = descr)
    
    exit(0)


if __name__ == "__main__":
    main()