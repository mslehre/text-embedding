import os
import sys
from pathlib import Path
import argparse
import numpy as np
import h5py
from compute_embedding import embedding_from_string


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
        pubs.append(lines[0])
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
                matching_entries = np.asarray(ids[:] == id).nonzero()[0]
                if len(matching_entries) > 1:
                    print ("WARNING: There are multiple entries for author ", 
                           id, file=sys.stderr)
                if len(matching_entries) != 0:  
                    # overwrite old embedding with the new one
                    index = matching_entries[0]
                    pub_embeddings[index, :] = embedding
                else:  # add new author
                    n = len(ids)
                    # resize datasets
                    ids.resize(n + 1, axis = 0)
                    pub_embeddings.resize(n + 1, axis = 0)
                    # add new author at the end of the datasets
                    ids[n] = id
                    pub_embeddings[n, :] = embedding
