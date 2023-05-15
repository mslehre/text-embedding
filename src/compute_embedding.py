import pandas as pd
import numpy as np
import tiktoken
import os
from openai.embeddings_utils import get_embedding

def embedding_from_string(string: str, embedding_name: str, encoding_name: str, max_tokens: int = 8191) -> list[float]:
    """Computes the embedding of a list of tokens"""
    # check if number of tokens is too large to compute embedding
    if(max_tokens > 8191):
        print('Your specified number of maximum number of tokens is larger than the maximum number of tokens', embedding_name, 'supports, which is', 8191, 'tokens.')
        return
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(string)
    if(len(tokens) > max_tokens):
        print('The number of your input tokens is', len(tokens), 'and exceeds the maximum number of tokens which is', max_tokens,'.')
        return
    if(os.environ.get('OPENAI_API_KEY') is None):
        print('You did not set your openai api key as environment variable. Therefore the embedding cannot be computed. Please set your key as environment variable by tiping: export OPENAI_API_KEY=\'your key\'.')
        return
    embedding_string = get_embedding(string, engine=embedding_name)
    embedding_token = get_embedding(np.array(tokens), engine=embedding_name)
    if(embedding_string == embedding_token):
        print('True')

    

embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"
max_token = 8000
for text in ["You are a big boy",
             "incomprehensibilities",
             "ich", "Ich",
             "er",
             "ist",
             ".", "?", ",",
             "er ist ich."]:
    embedding = embedding_from_string(text, embedding_model, embedding_encoding)
    print(embedding)