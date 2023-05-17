import pandas as pd
import numpy as np
import tiktoken
import os
import openai
from openai.embeddings_utils import get_embedding
from tokenizer import get_token_from_string 

def embedding_from_string(string: str, embedding_name: str, encoding_name: str, max_token: int = 8191) -> list[float]:
    """
    computes embedding from a string
    input: string
    output: embedding for string (1536 dimensional float vector)
    """
    # check if number of tokens is too large to compute embedding
    if(max_token > 8191):
        print('Your specified number of maximum number of tokens is larger than the maximum number of tokens', embedding_name, 'supports, which is', 8191, 'tokens.')
        return [None] # return None if user specifies maximum number of tokens that exceeds maximum token number of text-embedding-ada-002   
    tokens = get_token_from_string(string, max_token = max_token, force_cut = True,verbose = True)
    if(tokens is None):
        print('WARNING: The number of tokens for', string, 'exceeds the maximum number of tokens which is', max_token,'.')
        return [None] # return None if number of tokens is larger than maximum number of tokens
    # test if OPENAI_API_KEY is set as environment variable   
    if(os.environ.get('OPENAI_API_KEY') is None):
        print('You did not set your openai api key as environment variable. Therefore the embedding cannot be computed. Please set your key as environment variable by tiping: export OPENAI_API_KEY=\'your key\'.')
        return [None] # return None if openai key is not set as environment variable
    return get_embedding(string, engine=embedding_name)
   
def main():
    text = ["You are a big boy",
             "incomprehensibilities",
             "ich", "Ich",
             "er",
             "ist",
             ".", "?", ",",
             "er ist ich."]
    for t in text:
        print(t,"\nFirst five values of embedding for text:")
        embeddings = embedding_from_string(t, "text-embedding-ada-002", "cl100k_base")
        print(embeddings[0:5])
    exit(0)

if __name__ == "__main__":
    main()