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
              k: int = 5) -> list[int]:
    """Gets the IDs of the k chunks that have the best cosine similarity with 
    the embedded question. The embeddings of the chunks are given in the hdf5
    file named after the string of 'embeddings_file' which should be locaded in
    the data directory of this repository. The function gives back a list that 
    contains the IDs of the k best chunks starting with the best match for the 
    question.

    Args:
        question (str): The string of the question to compare the embeddings 
            of the chunks to.
        embeddings_file (str): The relative path of the hdf5 file, that 
            contains the embeddings , if one is currently in the data 
            directory, since all data files should be stored there. 
            Example:    For the file named "example_embeddings" in the  
                        directory "data/folder" the strings should be in the 
                        following format: "foler/example_embeddings" 
                        (without "/" at the beginning)
        k (int): Integer that indicates the number of chunks that are returned.   

    Returns:
        list[int]: The list that contains the IDs of the k files with the 
            best cosine similiarity for the question orderd from most to least 
            similar.
    """
    # Get the embeddings from the hpf5 file:
    file_path = os.getcwd() + "//../data/" + embeddings_file
    with h5py.File(file_path, 'r') as f_in:
        # get all embeddings and the id list:
        for key in f_in.keys():
            print(key)
            if("embeddings" in key):
                embeddings = f_in[key][:] 
            elif("ids" in key):
                id_list = f_in[key][:]
            else:
                print("Some keys of the hdf5 file could not be used.")


    # Compute IDs of the best embeddings and return the sorted list from 
    # biggest to smallest similarity:
    # Attention: embeddings with None in it are not given to the function which
    #            means that the resulting indices are not the right ones as 
    #            some embeddings were deletet.
    inds = get_embeddings_argsort(question=question, 
                                  embedding_list=embeddings)
    inds = [id_list[i] for i in inds] 
    # TODO: catch exception that k is bigger than number of chunks...
    return inds[0:k]

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
    question_embedding = embedding_from_string(string=question)
    similarities = []
    for i in range(0,len(embedding_list)):
        similarities.append(cosine_similarity(question_embedding, 
                                              embedding_list[i]))
    
    # Return the indices of the k best embeddings, the best results have the 
    # biggest cosine similarity.
    inds = np.array(similarities).argsort()[::-1]  
    return inds


def main():
    """Main to test the function that gets the k best chunks for a question.
    """
    question = "What papers did Daniel write?"
    k = 3
#    a = get_k_chunks_from_folder(question=question,
#                                 folder="Example_chunks",
#                                 k=k)
    a = get_k_IDs(question, 
                embeddings_file="example_pubs/example_embeddings.hdf5", k=k)
    if k == 1:
        print(f'Question: {question} The best file is {a[0]}.')
    else:
        print(f'Question: {question} The list with the best {k} files is {a}.')

    exit(0)

if __name__ == "__main__":
    main()