import os
import sys
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from compute_embedding import embedding_from_string


def embeddings_ids_from_file_list(file_list: list[str],
                             embedding_name: str = 'text-embedding-ada-002',
                             max_token: int = 8191
                             ) -> tuple[list[list[float]], list[str]]:
    """
    Get the embeddings and ids of the text files that are given in a list. The
    names of the files should be in the format <chunk_id>.txt.

    Args:
        file_list (list[str]): List that contains the paths of text files that
            should be embedded.
        embedding_name (str): The name of the embedding model. By default the
            model text-embedding-ada-002 is used.
        max_token (int): The maximum number of tokens for which an embedding is
            computed. By default this is the maximum number of tokens of the 
            embedding model text-embedding-ada-002.
        
    Returns:
        list[list[float]]: Embeddings of the given text files as a list, 
            each entry represents a file of the given list.
        list[str]: List of the ids of the files that were used for the 
            embeddings. The i-th id corresponds to the i-th entry of the 
            embeddings list.

    """
    embeddings = []
    ids = []

    for file_path in file_list:
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            with open(file_path, 'r') as file_handle:
                file_name = os.path.basename(file_path)
                stem = Path(file_name).stem
                suffix = Path(file_name).suffix

                if ("meta" in stem or "info" == stem or suffix != ".txt"):
                    print(f'file {file_path} cannot be used')
                    continue
                ids.append(str(stem))

                text = file_handle.read()
                embedding = embedding_from_string(text)

                if embedding == [None]:
                    print("ERROR: The embedding for \"", text, "\" could not "
                          + "be computed! Please check your input and "
                          + "parameters!")
                    exit(1)
                embeddings.append(embedding)

    return embeddings, ids

def file_paths_from_dir(dir_path: str) -> list[str]:
    """
    Get the file paths of the text files that are given in a directory. All 
    text files that are located in the given directory or any sub directory are
    selected. Only files with the format '*.meta.txt' or 'info.txt', that 
    contain other information, are ignored. The names of the text files should
    be in the format <chunk_id>.txt.

    Args:
        dir_path (str): Path to directory containing the text files/ chunks.
        embedding_name (str): The name of the embedding model. By default the
            model text-embedding-ada-002 is used.
        max_token (int): The maximum number of tokens for which an embedding is
            computed. By default this is the maximum number of tokens of the 
            embedding model text-embedding-ada-002.
        
    Returns:
        list[str]]: Paths of the text files as a list, each entry represents a
        file of the given directory (including sub diectories).
    """
    dir_path = os.path.join(dir_path, '')  # append '/' if not already there
    file_list = os.listdir(dir_path) # get all file and directory names
    all_file_paths = []

    for file_name in file_list:  # loop over all possible files and directories 
        path = os.path.join(dir_path, file_name)

        if(os.path.isfile(path)):
            stem = Path(file_name).stem
            suffix = Path(file_name).suffix

            if ("meta" in stem or "info" == stem or suffix != ".txt"):
                print(f'file {path} cannot be used')
                continue
            all_file_paths.append(path)
            
        elif(os.path.isdir(path)):
            all_file_paths += file_paths_from_dir(path)

        elif(not os.access(path, os.R_OK)):
            print(f'WARNING: the path {path} can nor be accesed.')

    return all_file_paths


def write_hdf5(hdf5_file: str,
               embeddings: list[list[float]],
               ids: list[str],
               update: bool = False):
    """
    Write embeddings to HDF5 file. Either write a new file or update an 
    existing one.

    Args:
        hdf5_file (str): Path to HDF5 file.
        embeddings (list[list[float]]): List with embeddings, each entry 
            represents an embedding of a chunk.
        ids (list[str]): List containing the IDs for each chunk that was 
            embedded.
        update (bool): If True, update an existing file with the data, else 
            write a new one.
    """
    embeddings = pd.DataFrame(embeddings)
    ids = pd.DataFrame(ids)

    if update:  # update existing hdf5 file
        hdf = pd.HDFStore(hdf5_file, mode='r')
        embeddings_old = pd.read_hdf(hdf, "embeddings") 
        ids_old = pd.read_hdf(hdf, "ids")
        hdf.close()

        for id, embedding in zip(ids[0], embeddings.values):
            # check if id is in dataset
            matching_entries = np.asarray(ids_old[0] == id).nonzero()[0]
            if len(matching_entries) > 1:
               print("WARNING: There are multiple entries for the chunk ", 
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

