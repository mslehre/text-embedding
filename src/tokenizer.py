import tiktoken

# gets tokens for a string
# input: string
# output: list with tokens for string
def tokens_from_string(string: str, encoding_name = "cl100k_base", max_token = 8000, force_cut = False, verbose = False) -> list[int]:
    encoding = tiktoken.get_encoding(encoding_name)
    token = encoding.encode(string)
    if len(token) > max_token: 
        if verbose:  # print warning if max tokens is exceeded
    	    print("WARNING: Number of tokens for string \""+string+"\" exceed the maximal number of tokens:", max_token, "!")
        if force_cut:  # cut off tokens after max number of tokens
    		return token[:max_token]
    	return [None]  # return None if number of tokens exceed maximal number of tokens
    return token

# gets tokens for a list of strings
# input: list of strings "chunks"
# output: list of list with tokens for strings
def tokens_for_chunks(chunks: list[str], encoding_name = "cl100k_base", max_token = 8000, force_cut = False, verbose = False) -> list[list[int]]:
    chunk_tokens = []
    for chunk in chunks:
        tokens = tokens_from_string(chunk, encoding_name = encoding_name, max_token = max_token, force_cut = force_cut, verbose = verbose)
        chunk_tokens.append(tokens)
    return chunk_tokens

def main():
    text = ["You are a big boy",
             "incomprehensibilities",
             "Me"]
    print("Text to encode:")
    for t in text:
    	print(t)
    encoded_text = tokens_for_chunks(text, verbose = True)
    print("Tokens for text:")
    for encoding in encoded_text:
        print(encoding)
    exit(0)

if __name__ == "__main__":
    main()
