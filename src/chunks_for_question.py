import tokenizer
#from compute_embedding import get_embedding

# What to think about:
#   - how to get the chunks? -> from folder, directly?
#   - get only tokens for each chunk or the text itself?
#   - how to return the chunks: indices, directly, which format?
#   - questiona as string or only tokens? both?

def get_k_chunks_for_string(question: str, 
                            k: int):
    """Gets the k chunks that have the best cosine similarity with the
    tokenized question.

    Args:
        question (str): The string of the question to scompare the embeddings 
            of the chunks to.
        k (int): Integer that indicates the number of chunks that are returned.


    Returns:
        LIST? VECTOR? ONLY INDICES?
    """
    pass

def main():
    """Main to test the function that gets the k best chunks for a question.
    """
    question = "What are the similarities of a banana and an apple?"
    tokens_quest = tokenizer.get_token_from_string(question)
    print(tokens_quest)
    exit(0)

if __name__ == "__main__":
    main()