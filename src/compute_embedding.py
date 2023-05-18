import os

import tiktoken
import openai
from openai.embeddings_utils import get_embedding

from tokenizer import get_token_from_string 

def embedding_from_string(string: str,
                          embedding_name: "text-embedding-ada-002",
                          max_token: int = 8191) -> list[float]:
    """This function computes the embedding for a string.

    Args:
        string (str): This parameter is the string of which the embedding is 
            computed.
        embedding_name (str): The name of the embedding model. By default the
            model text-embedding-ada-002 is used.
        max_token (int): The maximum number of tokens for which an embedding is
            computed. By default this is the maximum number of tokens of the 
            embedding model text-embedding-ada-002.

    Returns: 
        list[float]: The embedding for the string is returned as vector. In case
            of text-embedding-ada-002 as embedding model the dimension is 1536.
            If no embedding can be computed because the embedding model cannot
            be accessed or the number of tokens for the string that an embedding
            should be computed of is too large None is returned.
    """
    # Check if number of tokens is too large to for default embedding model.
    if (max_token > 8191):
        print('Your specified number of maximum number of tokens is larger \
            than the maximum number of tokens', embedding_name, 'supports, \
            which is', 8191, 'tokens.')
        return [None] 
    # Get tokens from string to test whether number of tokens is too large for 
    # the string.
    tokens = get_token_from_string(string, max_token=max_token, force_cut=True,
                                   verbose=True)
    if (tokens is None):
        print('WARNING: The number of tokens for', string, 'exceeds the \
            maximum number of tokens which is', max_token,'.')
        return [None]

    # Test if OPENAI_API_KEY is set as environment variable.  
    if (os.environ.get('OPENAI_API_KEY') is None):
        print('You did not set your openai api key as environment variable. \
            Therefore the embedding cannot be computed. Please set your key as \
            environment variable by typing: export OPENAI_API_KEY=\'your key\'\
            .')
        return [None]
    return get_embedding(string, engine=embedding_name)
   
def main():
    """This is the main function. If this program is executed the embedding for
    a few strings in a list is computed and both the string and the first five 
    values of its embedding are printed.
    """
    text = ["You are a big boy",
             "incomprehensibilities",
             "ich", "Ich",
             "er",
             "ist",
             ".", "?", ",",
             "er ist ich."]
    for t in text:
        print(t,"\nFirst five values of embedding for text:")
        embeddings = embedding_from_string(t)
        print(embeddings[0:5])
    exit(0)

if __name__ == "__main__":
    main()
