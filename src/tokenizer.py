import tiktoken

# gets tokens for a string
# input: string
# output: list with tokens for string
def tokens_from_string(string: str, encoding_name: str) -> list[int]:
    encoding = tiktoken.get_encoding(encoding_name)
    return encoding.encode(string)

# gets tokens for a list of strings
# input: list of strings "chunks"
# output: list of list with tokens for strings
def tokens_for_chunks(chunks: list[str], encoding_name = "cl100k_base") -> list[list[int]]:
    chunk_tokens = []
    for chunk in chunks:
        tokens = tokens_from_string(chunk, encoding_name)
        chunk_tokens.append(tokens)
    return chunk_tokens

def main():
    text = ["You are a big boy",
             "incomprehensibilities",
             "ich", "Ich",
             "er",
             "ist",
             ".", "?", ",",
             "er ist ich."]
    print("Text to encode:", text)
    encoded_text = tokens_for_chunks(text)
    print("Encoding:")
    for encoding in encoded_text:
        print(encoding)
    exit(0)

if __name__ == "__main__":
    main()