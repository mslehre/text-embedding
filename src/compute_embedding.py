import pandas as pd
import tiktoken
from openai.embeddings_utils import get_embedding

def embedding_from_string(string: str, embedding_name: str, encoding_name: str, max_tokens: int) -> list[float]:
    """Computes the embedding of a list of tokens"""
    # check if number of tokens is too large to compute embedding
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(str)
    if(len(tokens) > max_tokens):
        print('The number of your input tokens is', len(tokens), 'and exceeds the maximum number of tokens which is', max_tokens,'.')
        return
    return get_embedding(string, engine=embedding_name)

embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"
max_token = 8000
embedding = embedding_from_tokens(tokens, embedding_model, embedding_encoding, max_token)