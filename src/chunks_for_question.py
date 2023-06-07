import os

import h5py
import numpy as np
from compute_embedding import embedding_from_string
from openai.embeddings_utils import cosine_similarity

# TODO:
#   - catch exceptions if wrong file  does not exist
#   - catch exceptions if no arguments are given (e.g. no file,...)

def get_k_IDs(question: str,
              embeddings_file: str,
              k: int) -> list[int]:
    """Gets the IDs of the k chunks that have the best cosine similarity with 
    the embedded question. The embeddings of the chunks are given in the hdf5
    file embeddin_file which should be locaded in the data directory of this
    repository. The function gives back a list that contains the IDs of the k
    best chunks starting with the best match for the question.
    ATTENTION: At this point it only returns the indices, not IDs. It may be
               added later.

    Args:
        question (str): The string of the question to scompare the embeddings 
            of the chunks to.
        embeddings_file (str): The relative path of the hdf5 file, that 
            contains the embeddings , if one is currently in the data 
            directory, since all data files should be stored there. 
            Example:    For the file named "example_embeddings" in the data 
                        directory the strings should be in the following 
                        format: "example_embeddings" (without "/" at the 
                        beginning)
            If the file is stored in another folder, then use the relative 
            path without "/" at the beginning. (e.g. "folder/file_name")
        k (int): Integer that indicates the number of chunks that are returned.   

    Returns:
        list[int]: The list that contains the IDs of the k files with the 
            best cosine similiarity for the question orderd from most to least 
            similar.
    """
    # Get the embeddings from the hpf5 file:
    file_path = os.getcwd() + "../data/" + embeddings_file
    with h5py.File(file_path, 'r') as f_in:
        file_keys = f_in.keys()
        # get all embeddings, shoulb be list of lists:
        embeddings_all = f_in[file_keys[0]][:] 

    # Filter out embeddings that are None and save indices/IDs of selected 
    # embeddings:
    embeddings = []  # empty list for embeddings that exist
    ids = []  # list for indices/IDs of embeddings that exist
    for i in range(0, len(embeddings_all)):
        if(all(embeddings_all[i]) is not None):
            embeddings.append(embeddings_all[i])
            ids.append(i)
        else:
            print("A chunk could not be used as it was not computed.")

    # Compute IDs of the best embeddings and return the sorted list from 
    # biggest to smallest similarity:
    # Attention: embeddings with None in it are not given to the function which
    #            means that the resulting indices are not the right ones as 
    #            some embeddings were deletet.
    inds = get_embeddings_argsort(question=question, 
                                  embedding_list=embeddings)
    inds = [ids[i] for i in inds] 

    # TODO: catch exception that k is bigger than number of chunks...
    
    return inds[0:k]

    
# For now leave the function here for test purposes, may delete later...:
def get_k_chunks_from_folder(question: str = "What is a pizza?", 
                             folder: str = "Example_chunks",
                             k: int = 1) -> list[str]:
    """Gets the k chunks that have the best cosine similarity with the
    embedded question. The analysed chunks are taken from the named folder, 
    every file in this folder is embedded and compared to the embedded 
    question.

    Args:
        question (str): The string of the question to scompare the embeddings 
            of the chunks to.
        folder (str): The relative path of the folder if one is currently in 
            the data directory, since all data should be stored there.#
            Example:    For the folder named "Example_chunks" in the data 
                        directory the strings should be in the following 
                        format: "Exampe_chunks" (without "/" at thebeginning)
            If the folder is stored in another folder, then use the relative 
            path without "/" at the beginning.
        k (int): Integer that indicates the number of chunks that are returned.
            Default is set to 1 chunks for now.     

    Returns:
        list[str]: The list that contains the names of the k files with the 
            best cosine similiarity for the question orderd from most to least 
            similar.
    """
    # TODO: catch exceptions if k=0, No question, ...
    # Embed the different chunks and compute cosine similarity with question:
    directory = os.getcwd() + "/../data/" + folder
    file_list = os.listdir(directory)
    string_list = []

    for filename in file_list:
        # TODO: catch exceptions of wrong files/ folders...
        with open(directory + "/" + filename,'r') as f_in:
            data = f_in.read().replace('\n', ' ')  # linebreaks to whitespaces
            string_list.append(data)
    
    chunks_embedding = []
    for i in range(0,len(string_list)):
        chunks_embedding.append(embedding_from_string(string=string_list[i]))
    
    # Get indices of best embeddings and return the filenames of the 
    # corresponding files.
    inds = get_embeddings_argsort(question=question,
                                        embedding_list=chunks_embedding)
    
    return [file_list[i] for i in inds[0:k]]

def get_embeddings_argsort(question: str, 
                           embedding_list: list[list[float]]) -> list[int]:
    """Gets the argsort of the given embeddings from best cosine similarity to 
    least similarity with the given question.

    Args:
        question (str): The string of the question that is compared to the 
            embeddings of the chunks.
        embedding_list (list[list[float]]): The list containing the embeddings 
            of the chunks.   

    Returns:
        list[int]: The list that contains the indices of the argsort of the 
            embeddings according to the cosine similiarity for the question 
            orderd from most to least similar.
    """
    # Embed the question
    quest_embedding = embedding_from_string(string=question)
    similarities = []
    for i in range(0,len(embedding_list)):
        similarities.append(cosine_similarity(quest_embedding, 
                                              embedding_list[i]))
    
    # Return the indices of the k best embeddings, the best results have the 
    # biggest cosine similarity.
    inds = np.array(similarities).argsort()[::-1]  
    return inds


def main():
    """Main to test the function that gets the k best chunks for a question.
    """
    question = "What is a pizza?"
    k = 1
    a = get_k_chunks_from_folder(question=question,
                                 folder="Example_chunks",
                                 k=k)
    if k == 1:
        print(f'Question: {question} The best file is {a[0]}.')
    else:
        print(f'Question: {question} The list with the best {k} files is {a}.')

    exit(0)

if __name__ == "__main__":
    main()