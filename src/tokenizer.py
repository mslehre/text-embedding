import tiktoken

def get_token_from_string(string: str, 
                          encoding_name: str = "cl100k_base", 
                          max_token: int = 8000, 
                          force_cut: bool = False, 
                          verbose: bool = False) -> list[int]:
    """
    Gets the tokens for a string.
    
    Args:
        string (str): The string of which the tokens are computed.
        encoding_name (str): Name of the encoding model. The default encoding
            model should always be the same as the default encoding model of
            get_string_from_tokens.
        max_token (int): Max allowed length of the token list if force_cut is 
            set to True. 
        force_cut (bool): If True, cuts off tokens after max number of token. 
            If False, returns None if number of tokens exceeds maximal number 
            of token.
        verbose (bool): If True, prints out more information.

    Returns:
        list[int]: List with the tokens for the string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    token = encoding.encode(string)
    if len(token) > max_token: 
        if verbose:  # print warning if max number of tokens is exceeded
            print("WARNING: Number of tokens for string \"" + string + 
                  "\" exceeds the maximal number of tokens:", max_token, "!")
        if force_cut:  # cut off tokens after max number of token
    	    return token[:max_token]
        return [None]  # return None if number of tokens exceeds maximal number
    return token

def get_token_for_chunks(chunks: list[str], 
                         encoding_name: str = "cl100k_base", 
                         max_token: int = 8000, 
                         force_cut: bool = False, 
                         verbose: bool = False) -> list[list[int]]:
    """
    Gets tokens for a list of strings.

    Args:
        chunks (list[str]): List of strings for the computation of tokens.
        encoding_name (str): Name of the encoding model. The default encoding
            model should always be the same as the default encoding model of
            get_token_from_string.
        max_token (int): Max allowed length of the token list if force_cut is 
            set to True. 
        force_cut (bool): If True, cuts off tokens after max number of token. 
            If False, returns None if number of tokens exceeds maximal number 
            of token.
        verbose (bool): If True, prints out more information.
    
    Returns:
        list[list[int]]: List of list with the tokens for strings.
    """
    chunk_token = []
    for chunk in chunks:
        token = get_token_from_string(string=chunk, 
                                      encoding_name=encoding_name,
                                      max_token=max_token, 
                                      force_cut=force_cut, 
                                      verbose=verbose)
        chunk_token.append(token)
    return chunk_token

def get_string_from_tokens(token: list[int], 
                           encoding_name: str = "cl100k_base") -> str:
    """
    Gets the string that tokens encode.

    Args:
        token (list[int]): The tokens which should be decoded to the string they
            encode.
        encoding_name (str): Name of the encoding model. The encoding model is 
            also needed to decode the tokens. The default encoding model should
            always be the same as the default encoding model of 
            get_token_from_string.
    
    Returns:
        str: The string that the tokens encode.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return encoding.decode(token)

def main():
    text = ["You are a big boy",
             "incomprehensibilities",
             "Me!"]
    print("Text to encode:")
    for t in text:
        print(t)
    encoded_text = get_token_for_chunks(text, verbose=True)
    print("Tokens for text:")
    for encoding in encoded_text:
        print(encoding)
    exit(0)

if __name__ == "__main__":
    main()
