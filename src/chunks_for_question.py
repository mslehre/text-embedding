import os

import numpy as np
from compute_embedding import embedding_from_string
from openai.embeddings_utils import cosine_similarity

# What to think about:
#   - how to get the chunks? -> from folder, directly?
#   - how to return the chunks: indices, directly, which format?
#   - questiona as string or only tokens? both?
#   - catch exceptions if wrong folder is named or not only target files in 
#     there

def get_k_chunks_from_folder(question: str, 
                             folder: str,
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
    # Embed the different chunks and compute cosine similarity with question:
    directory = os.getcwd() + "/../data/" + folder
    file_list = os.listdir(directory)
    string_list = []

    for filename in file_list:
        # TODO: catch exceptions of wrong files/ folders...
        with open(directory + "/" + filename,'r') as file:
            data = file.read().replace('\n', ' ')  # linebreaks to whitespaces
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
                             embedding_list: list[float]) -> list[int]:
    """Gets the argsort of the given embeddings from best cosine similarity to 
    least similarity with the given question.

    Args:
        question (str): The string of the question to scompare the embeddings 
            of the chunks to.
        embedding_list (list[float]): The list containing the embeddings of the
            chunks.   

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