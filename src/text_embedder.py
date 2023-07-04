import os
import sys
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
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
        pubs.append(lines[0].split(',')[0])  # extract author name 
        for line in lines[1:]:
            if line.strip():  # check if line is not empty
                pubs.append(line)
    author_pubs = "\n".join(pubs)

    return author_pubs

def read_pubs_in_dir(dir_path: str, 
              n: int) -> tuple[list[str], pd.DataFrame]:
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
        author_ids (pd.DataFrame): DataFrame of author ids corresponding to
            the publication lists.
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

    author_ids = pd.DataFrame(author_ids)
    return pubs, author_ids

def embeddings_from_pubs(pubs: list[str], 
                         embedding_name: str = 'text-embedding-ada-002',
                         max_token: int = 8191 ) -> pd.DataFrame:    
    """
    Get the embeddings of the publications for every author.

    Args:
        pubs (list[str]): List of strings containing the publication titles.
        embedding_name (str): The name of the embedding model. By default the
            model text-embedding-ada-002 is used.
        max_token (int): The maximum number of tokens for which an embedding is
            computed. By default this is the maximum number of tokens of the 
            embedding model text-embedding-ada-002.
        
    Returns:
        embeddings (pd.DataFrame): Embeddings of the publication lists as a
            pandas DataFrame, each row represents an embedding od an author.
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

    embeddings = pd.DataFrame(embeddings)
    return embeddings

def write_hdf5(hdf5_file: str,
               embeddings: pd.DataFrame,
               ids: pd.DataFrame,
               update: bool = False):
    """
    Write embeddings to HDF5 file. Either write a new file or update an 
    existing one.

    Args:
        hdf5_file (str): Path to HDF5 file.
        embeddings (pd.DataFrame): Pandas DataFrame with embeddings, each 
            row represents an embedding of a chunk.
        ids (pd.DataFrame): Pandas DataFrame containing the IDs for each 
            embedding of a chunk.
        update (bool): If True, update an existing file with the data, else 
            write a new one.
    """
    if update:  # update existing hdf5 file
        hdf = pd.HDFStore(hdf5_file, mode='r')
        embeddings_old = pd.read_hdf(hdf, "embeddings") 
        ids_old = pd.read_hdf(hdf, "ids")
        hdf.close()

        for id, embedding in zip(ids[0], embeddings.values):
            # check if id is in dataset
            matching_entries = np.asarray(ids_old[0] == id).nonzero()[0]
            if len(matching_entries) > 1:
               print ("WARNING: There are multiple entries for the chunk ", 
                       id, file=sys.stderr)
            if len(matching_entries) != 0:  
                # overwrite old embedding with the new one
                index = matching_entries[0]
                embeddings_old.iloc[index] = embedding
                embeddings = embeddings_old
                ids = ids_old
            else:  # add new chunk id at the end of the datasets
                ids = pd.concat([ids_old,pd.DataFrame([id])])
                embeddings = pd.concat([embeddings_old,
                                        pd.DataFrame([embedding])])

    hdf = pd.HDFStore(hdf5_file, mode='w') # new file or overwrite old file
    hdf.put('embeddings', embeddings, format='table', append = False)
    hdf.put('ids', ids, format='table', append=False)
    hdf.close()

