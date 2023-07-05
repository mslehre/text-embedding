import os
import sys
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from compute_embedding import embedding_from_string


def read_text_from_file(file_path: str) -> str:
    """
    Read a text from a file/chunk into a string.

    Args:
        file_path (str): Path to file/chunk with the text.

    Returns:
        text (str): String that contains the text from the chunk".
    """
    with open(file_path, 'r') as file_handle:
        text = file_handle.read()

    return text

def read_texts_in_dir(dir_path: str) -> tuple[list[str], pd.DataFrame]:
    """
    Read all text files in a directory into a list of strings.

    Args:
        dir_path (str): Path to directory containing files with the chunks.
            The names of the files should be in the format <chunk_id>.txt.
            Every file in this format is used, files with format '*.meta.txt'
            or 'info.txt' are ignored. If the directory contains sub
            directories, e.g. for examination regulations, all format fitting
            files in all sub directories will be used. make sure, that ONLY 
            text files that should be embedded are located in this (these)
            directory (directories).

    Returns:
        string_list (list[str]): List that contains the strings from the text 
            files.
        ids (pd.DataFrame): DataFrame of chunk ids corresponding to the text 
            files.
    """
    print("read texts from directory")

    dir_path = os.path.join(dir_path, '')  # append '/' if not already there
    string_list = []
    ids = []
    file_list = os.listdir(dir_path) # get all files in the directory

    for file in file_list:  # loop over all possible files
        file_stem = Path(file).stem
        file_suffix = Path(file).suffix
        file_path = os.path.join(dir_path, file)
        if("meta" in file_stem or "info" == file_stem or file_suffix != ".txt"):
            print(f'file {file} cannot be used')
            break
        id = str(file_stem)
        #print(id)

        # check if file exists and is readable, if yes read
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            ids.append(id)  # save ID
            text = read_text_from_file(file_path)  # read file
            string_list.append(text)

            #print(text[0:30])

    ids = pd.DataFrame(ids)
    return string_list, ids

def embeddings_from_list_of_strings(string_list: list[str], 
                         embedding_name: str = 'text-embedding-ada-002',
                         max_token: int = 8191 ) -> pd.DataFrame:    
    """
    Get the embeddings of the strings that are given in a list.

    Args:
        string_list (list[str]): List of strings that will be embedded.
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

    for text in string_list:
        embed = embedding_from_string(text,
                                      embedding_name = embedding_name,
                                      max_token = max_token)
        if embed == [None]:
            print("ERROR: The embedding for \"", text, "\" could not be" 
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

