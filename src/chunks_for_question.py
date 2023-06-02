import os

import tokenizer
from compute_embedding import get_embedding

# What to think about:
#   - how to get the chunks? -> from folder, directly?
#   - how to return the chunks: indices, directly, which format?
#   - questiona as string or only tokens? both?
#   - catch exceptions if wrong folder is named or not only target files in 
#     there

def get_k_chunks_from_folder(question: str, 
                             folder: str,
                             k: int = 3) -> list[str]:
    
    """Gets the k chunks that have the best cosine similarity with the
    tokenized question. The analysed chunks are taken from the named folder, 
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
            Default is set to 3 chunks for now.     

    Returns:
        list[str]: The list that contains the names of the k files with the 
            best cosine similiarity for the question orderd from best to least 
            similar.
    """
    directory = os.getcwd() + "/../data/" + folder
    for filename in os.listdir(directory):
        # TODO: catch exceptions of wrong files/ folders...
        print(filename)

def main():
    """Main to test the function that gets the k best chunks for a question.
    """
    question = "What are the similarities of a banana and an apple?"
    tokens_quest = tokenizer.get_token_from_string(question)
    a = get_k_chunks_from_folder(question="What color has an apple?",
                                 folder="Example_chunks",
                                 k=1)
    print(tokens_quest)
    exit(0)

if __name__ == "__main__":
    main()