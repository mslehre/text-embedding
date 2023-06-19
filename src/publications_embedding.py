#!/usr/bin/env python3

import os
from pathlib import Path
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

def try_to_read_file(file_path: str) -> str:
    # a quick function for argparse to check if given arg is a readable file
    if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
        raise argparse.ArgumentTypeError("The file " + file_path + "does not "
                                         + "exist or is not readable!")
    return file_path

def try_to_write_file_if_exists(file_path: str) -> str:
    # a quick function for argparse to check if given arg is a writable file
    if os.path.isfile(file_path) and not os.access(file_path, os.W_OK):
        raise argparse.ArgumentTypeError("The file " + file_path + "is not "
                                         + "writable!")
    return file_path

def read_pub(file_path: str) -> str:
    """
    Read publication titles in a file into a string

    Args:
        file_path (str): Path to file with publications.

    Returns:
        author_pubs (str): All publications in a string joined by "; ".
    """
    pubs = []
    with open(file_path, 'r') as file_handle:
        lines = file_handle.readlines()
        for line in lines[1:]:  # exclude first line containing author
            if line.strip():  # check if line is not empty
                # add publication title and ignore link
                pubs.append(line.split('\t')[0])
    author_pubs = "; ".join(pubs)

    return author_pubs

def read_pubs_in_dir(dir_path: str, 
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

        # check if file exists and is readable, if yes read
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            author_ids.append(i)  # save ID
            author_pubs = read_pub(file_path)  # read file
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

def write_hdf5(hdf5_file: str,
               embeddings: np.ndarray,
               author_ids: np.ndarray,
               update: bool = False):
    
    if not update:  # write new hdf5 file
        with h5py.File(hdf5_file, 'w') as f:
            f.create_dataset(name = 'publication_embedding', 
                             data = embeddings,
                             maxshape = (None, None),  # dataset resizable
                             compression = 'gzip')
            f.create_dataset(name = 'author_ids', 
                             data = author_ids,
                             maxshape = (None,),  # dataset resizable
                             compression = 'gzip')

    else:  # update existing hdf5 file
        with h5py.File(hdf5_file, 'r+') as f:
            pub_embeddings = f['publication_embedding']
            ids = f['author_ids']
            for id, embedding in zip(author_ids, embeddings):
                # check if id is in dataset
                index = np.where(ids[:] == id)[0]
                if len(index) != 0:  # overwrite old embedding with the new one
                    index = index[0]
                    pub_embeddings[index, :] = embedding
                else:  # add new author
                    n = len(ids)
                    # resize datasets
                    ids.resize(n + 1, axis = 0)
                    pub_embeddings.resize(n + 1, axis = 0)
                    # add new author at the end of the datasets
                    ids[n] = id
                    pub_embeddings[n, :] = embedding

def main():
    parser = argparse.ArgumentParser(
        description='Compute embeddings for lists of publications.')
    parser.add_argument('-p', '--publications', type = try_to_read_dir,
                        metavar = 'DIR', 
                        help = 'Directory containing files with names ' 
                        + '<author_id>.txt, which contain publication lists.')
    parser.add_argument('-n', '--num_authors', type = int, metavar = 'INT',
                        help = 'Number of expected files in the publications ' 
                        + 'directory, i.e. if the highest author ID in the ' 
                        + 'directory is 10, specify 11 as the indexing starts '
                        + 'with 0. All files in {0.txt, ... n-1.txt} are ' 
                        + 'tried, a subset may be missing.')
    parser.add_argument('-u', '--update', nargs = '+', type = try_to_read_file,
                        metavar='FILE',
                        help = 'Update existing embeddings in hdf5 file with '
                        +' the publications in the specified file(s). The '
                        + ' names of the files must again have format '
                        + '<author_id>.txt. If the author ID already exists in'
                        + ' the HDF5 file, the corresponding embedding will be'
                        + ' overwritten, if not, it will be added to the '
                        + 'dataset. This option is mutually exclusive with '
                        + '\'--publications\'.')
    parser.add_argument('-f', '--hdf5_file', required = True,
                        type = try_to_write_file_if_exists,
                        help = 'Output file in hdf5 format with data sets: ' 
                        + 'publication_embedding: 2-dim numpy array with '
                        + 'embeddings. author_ids: 1-dim numpy array '
                        + 'containing the ids for each embedding.')
    args = parser.parse_args()

    # either compute new embedding or update existing embedding
    if (not args.publications and not args.update) or \
        (args.publications and args.update):
        print("ERROR: You need to specifiy exactly one of the 2 arguments: " 
              + "'--publications' or '--update'!!!")
        exit(1)
    # arguments --publications and --num_authors need to be specified together
    if args.publications and not args.num_authors:
        print("ERROR: You need to specify argument '--num_authors' with "
              + "argument '--publications'!!!")
        exit(1)
    # check if file to update exists
    if args.update and not os.path.isfile(args.hdf5_file):
        print("ERROR: File", args.hdf5_file, "does not exist!!! Please specify"
            + " a HDF5 file to update!")

    # compute embeddings for publications in directory
    if args.publications:
        # read publications and compute embeddings
        pubs, author_ids = read_pubs_in_dir(args.publications, 
                                            args.num_authors)
        embeddings = embeddings_from_pubs(pubs)
        # write data to hdf5 file
        write_hdf5(args.hdf5_file, embeddings, author_ids)
    
    else:  # update existing embedding
        author_ids = []
        pubs = []
        for file_path in args.update:
            # check if file names have format <author_id>.txt
            file_stem = Path(file_path).stem
            try:
                id = int(file_stem)
            except ValueError:
                print("ERROR: The name of file \"", file_path, "\" does not " 
                + "have format <author_id>.txt!!!")
                exit(1)
            # read if yes
            author_pubs = read_pub(file_path)
            author_ids.append(id)
            pubs.append(author_pubs)
        # compute embeddings            
        embeddings = embeddings_from_pubs(pubs)
        author_ids = np.asarray(author_ids)
        # update hdf5 file
        write_hdf5(args.hdf5_file, embeddings, author_ids, update = True)

    exit(0)


if __name__ == "__main__":
    main()
