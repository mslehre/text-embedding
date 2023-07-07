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
                    print(f'file {file_path} is ignored.')
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

def file_paths_from_list(path_list: list[str]) -> list[str]:
    """
    Get the file paths of the text files from a list of paths. If a path to a 
    directory is given in the path list, all text files that are located in the 
    directory or any sub directory are selected. Only files with the format 
    '*.meta.txt' or 'info.txt', that contain other information, are ignored. 
    The names of the text files should be in the format <chunk_id>.txt.

    Args:
        path_list (list[str]): List of paths for text files and directories 
            that contain text files/ chunks.
        embedding_name (str): The name of the embedding model. By default the
            model text-embedding-ada-002 is used.
        max_token (int): The maximum number of tokens for which an embedding is
            computed. By default this is the maximum number of tokens of the 
            embedding model text-embedding-ada-002.
        
    Returns:
        list[str]]: Paths of the text files as a list including text files that 
        are located in directories, sub diectories, ... from the path list.
    """
    all_file_paths = []

    for path in path_list :
        if(os.path.isfile(path)):  # if path is file
            suffix = Path(path).suffix
            if ("meta.txt" in path or "info.txt" in path or suffix != ".txt"):
                print(f'file {path} is ignored')
                continue
            all_file_paths.append(path)

        elif(os.path.isdir(path)):
                sub_paths = [os.path.join(path, sub_path) 
                             for sub_path in os.listdir(path)]
                all_file_paths += file_paths_from_list(sub_paths)

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

