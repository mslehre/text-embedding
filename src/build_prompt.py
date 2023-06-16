from tokenizer import get_token_from_string
from tokenizer import get_string_from_tokens

def get_prompt(
    query: str,
    chunks: dict,) -> str:
    """From a question and relevant documents, build the prompt to ask the LLM.

    Args:
        query (str): Question to ask the LLM.
        chunks (dict): Dictionary containing the text of the chunks as values.

    Returns:
        str: The completed prompt, combined from the template, query and chunks.
    """

    context = ""
    for key in chunks:
        context += chunks[key] + "\n"

    template=f"""You are a Bot assistant answering any questions about documents.
You are given a question and a set of documents.
If the user's question requires you to provide specific information from the documents, give your answer based only on the examples provided below. DON'T generate an answer that is NOT written in the provided examples.
If you don't find the answer to the user's question with the examples provided to you below, answer that you didn't find the answer in the documentation and propose him to rephrase his query with more details.
Use bullet points if you have to make a list, only if necessary.
Finish by proposing your help for anything else.

QUESTION: {query}

DOCUMENTS:
=========
{context}
=========
"""

    #tokenize to make sure the prompt does not exceed the token limit, cut it off if it does
    prompt_tokens = get_token_from_string(template,encoding_name="p50k_base", max_token=3500, force_cut=True, verbose=True)
    prompt = get_string_from_tokens(prompt_tokens, encoding_name="p50k_base")
    return prompt

def test():
    test_q = "a test"
    test_chunks = {'first': 'this is an apple', 'second': 'this is a banana', 'third': 'this is an orange'}
    testp = get_prompt(test_q, test_chunks)
    print(testp)